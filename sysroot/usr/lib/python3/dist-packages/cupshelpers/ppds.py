#!/usr/bin/python3

## system-config-printer

## Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2014, 2015 Red Hat, Inc.
## Copyright (C) 2006 Florian Festi <ffesti@redhat.com>
## Copyright (C) 2006, 2007, 2008, 2009 Tim Waugh <twaugh@redhat.com>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import cups
from .cupshelpers import parseDeviceID
from . import xmldriverprefs
import itertools
import string
import time
import locale
import os.path
import functools
import re
from . import _debugprint, set_debugprint_fn
from functools import reduce

__all__ = ['ppdMakeModelSplit',
           'PPDs']

_MFR_BY_RANGE = [
    # Fill in missing manufacturer names based on model name
    ("HP", re.compile("deskjet"
                      "|dj[ 0-9]?"
                      "|laserjet"
                      "|lj"
                      "|color laserjet"
                      "|color lj"
                      "|designjet"
                      "|officejet"
                      "|oj"
                      "|photosmart"
                      "|ps "
                      "|psc"
                      "|edgeline")),
    ("Epson", re.compile("stylus|aculaser")),
    ("Apple", re.compile("stylewriter"
                         "|imagewriter"
                         "|deskwriter"
                         "|laserwriter")),
    ("Canon", re.compile("pixus"
                         "|pixma"
                         "|selphy"
                         "|imagerunner"
                         "|bj"
                         "|lbp")),
    ("Brother", re.compile("hl|dcp|mfc")),
    ("Xerox", re.compile("docuprint"
                         "|docupage"
                         "|phaser"
                         "|workcentre"
                         "|homecentre")),
    ("Lexmark", re.compile("optra|(:color )?jetprinter")),
    ("KONICA MINOLTA", re.compile("magicolor"
                                  "|pageworks"
                                  "|pagepro")),
    ("Kyocera", re.compile("fs-"
                           "|km-"
                           "|taskalfa")),
    ("Ricoh", re.compile("aficio")),
    ("Oce", re.compile("varioprint")),
    ("Oki", re.compile("okipage|microline"))
    ]

_MFR_NAMES_BY_LOWER = {}
for mfr, regexp in _MFR_BY_RANGE:
    _MFR_NAMES_BY_LOWER[mfr.lower ()] = mfr

_HP_MODEL_BY_NAME = {
    "dj": "DeskJet",
    "lj": "LaserJet",
    "oj": "OfficeJet",
    "color lj": "Color LaserJet",
    "ps ": "PhotoSmart",
    "hp ": ""
}

_RE_turboprint = re.compile ("turboprint")
_RE_version_numbers = re.compile (r" v(?:er\.)?\d(?:\d*\.\d+)?(?: |$)")
_RE_ignore_suffix = re.compile (","
                                "| hpijs"
                                "| foomatic/"
                                "| - "
                                "| w/"
                                "| \\("
                                "| postscript"
                                "| ps"
                                "| pdf"
                                "| pxl"
                                "| zjs"         # hpcups
                                "| zxs"         # hpcups
                                "| pcl3"        # hpcups
                                "| printer"     # hpcups
                                "|_bt"
                                "| pcl"         # Canon CQue
                                "| ufr ii"      # Canon UFR II
                                "| br-script"  # Brother PPDs
                                )
_RE_ignore_series = re.compile (" series| all-in-one", re.I)

def ppdMakeModelSplit (ppd_make_and_model):
    """
    Split a ppd-make-and-model string into a canonical make and model pair.

    @type ppd_make_and_model: string
    @param ppd_make_and_model: IPP ppd-make-and-model attribute
    @return: a string pair representing the make and the model
    """

    # If the string starts with a known model name (like "LaserJet") assume
    # that the manufacturer name is missing and add the manufacturer name
    # corresponding to the model name
    ppd_make_and_model.strip ()
    make = None
    cleanup_make = False
    l = ppd_make_and_model.lower ()
    for mfr, regexp in _MFR_BY_RANGE:
        if regexp.match (l):
            make = mfr
            model = ppd_make_and_model
            break

    # Handle PPDs provided by Turboprint
    if make is None and _RE_turboprint.search (l):
        t = ppd_make_and_model.find (" TurboPrint")
        if t != -1:
            t2 = ppd_make_and_model.rfind (" TurboPrint")
            if t != t2:
                ppd_make_and_model = ppd_make_and_model[t + 12:t2]
            else:
                ppd_make_and_model = ppd_make_and_model[:t]
        try:
            make, model = ppd_make_and_model.split("_", 1)
        except:
            make = ppd_make_and_model
            model = ''
        make = re.sub (r"(?<=[a-z])(?=[0-9])", " ", make)
        make = re.sub (r"(?<=[a-z])(?=[A-Z])", " ", make)
        model = re.sub (r"(?<=[a-z])(?=[0-9])", " ", model)
        model = re.sub (r"(?<=[a-z])(?=[A-Z])", " ", model)
        model = re.sub (r" Jet", "Jet", model)
        model = re.sub (r"Photo Smart", "PhotoSmart", model)
        cleanup_make = True

    # Special handling for two-word manufacturers
    elif l.startswith ("konica minolta "):
        make = "KONICA MINOLTA"
        model = ppd_make_and_model[15:]
    elif l.startswith ("lexmark international "):
        make = "Lexmark"
        model = ppd_make_and_model[22:]
    elif l.startswith ("kyocera mita "):
        make = "Kyocera"
        model = ppd_make_and_model[13:]
    elif l.startswith ("kyocera "):
        make = "Kyocera"
        model = ppd_make_and_model[8:]
    elif l.startswith ("fuji xerox "):
        make = "Fuji Xerox"
        model = ppd_make_and_model[11:]

    # Finally, take the first word as the name of the manufacturer.
    else:
        cleanup_make = True
        try:
            make, model = ppd_make_and_model.split(" ", 1)
        except:
            make = ppd_make_and_model
            model = ''

    # Standardised names for manufacturers.
    makel = make.lower ()
    if cleanup_make:
        if (makel.startswith ("hewlett") and
            makel.endswith ("packard")):
            make = "HP"
            makel = "hp"
        elif (makel.startswith ("konica") and
              makel.endswith ("minolta")):
            make = "KONICA MINOLTA"
            makel = "konica minolta"
        else:
            # Fix case errors.
            mfr = _MFR_NAMES_BY_LOWER.get (makel)
            if mfr:
                make = mfr

    # HP and Canon PostScript PPDs give NickNames like:
    # *NickName: "HP LaserJet 4 Plus v2013.111 Postscript (recommended)"
    # *NickName: "Canon MG4100 series Ver.3.90"
    # Find the version number and truncate at that point.  But beware,
    # other model names can legitimately look like version numbers,
    # e.g. Epson PX V500.
    # Truncate only if the version number has only one digit, or a dot
    # with digits before and after.
    modell = model.lower ()
    v = modell.find (" v")
    if v != -1:
        # Look for " v" or " ver." followed by a digit, optionally
        # followed by more digits, a dot, and more digits; and
        # terminated by a space of the end of the line.
        vmatch = _RE_version_numbers.search (modell)
        if vmatch:
            # Found it -- truncate at that point.
            vstart = vmatch.start ()
            modell = modell[:vstart]
            model = model[:vstart]

    suffix = _RE_ignore_suffix.search (modell)
    if suffix:
        suffixstart = suffix.start ()
        modell = modell[:suffixstart]
        model = model[:suffixstart]

    # Remove the word "Series" if present.  Some models are referred
    # to as e.g. HP OfficeJet Series 300 (from hpcups, and in the
    # Device IDs of such models), and other groups of models are
    # referred to in drivers as e.g. Epson Stylus Color Series (CUPS).
    (model, n) = _RE_ignore_series.subn ("", model, count=1)
    if n:
        modell = model.lower ()

    if makel == "hp":
        for name, fullname in _HP_MODEL_BY_NAME.items ():
            if modell.startswith (name):
                model = fullname + model[len (name):]
                modell = model.lower ()
                break

    model = model.strip ()
    return (make, model)

def normalize (strin):
    """
    This function normalizes manufacturer and model names for comparing.
    The string is turned to lower case and leading and trailing white
    space is removed. After that each sequence of non-alphanumeric
    characters (including white space) is replaced by a single space and
    also at each change between letters and numbers a single space is added.
    This makes the comparison only done by alphanumeric characters and the
    words formed from them. So mostly two strings which sound the same when
    you pronounce them are considered equal. Printer manufacturers do not
    market two models whose names sound the same but differ only by
    upper/lower case, spaces, dashes, ..., but in printer drivers names can
    be easily supplied with these details of the name written in the wrong
    way, especially if the IEEE-1284 device ID of the printer is not known.
    This way we get a very reliable matching of printer model names.
    Examples:
    - Epson PM-A820 -> epson pm a 820
    - Epson PM A820 -> epson pm a 820
    - HP PhotoSmart C 8100 -> hp photosmart c 8100
    - hp Photosmart C8100  -> hp photosmart c 8100

    @type strin: string that can be the make or the model
    @return: a normalized lowercase string in which punctuations have been replaced with spaces.
    """
    lstrin = strin.strip ().lower ()
    normalized = ""

    BLANK=0
    ALPHA=1
    DIGIT=2
    lastchar = BLANK

    alnumfound = False
    for i in range (len (lstrin)):
        if lstrin[i].isalpha ():
            if lastchar != ALPHA and alnumfound:
                normalized += " ";
            lastchar = ALPHA
        elif lstrin[i].isdigit ():
            if lastchar != DIGIT and alnumfound:
                normalized += " ";
            lastchar = DIGIT
        else:
            lastchar = BLANK

        if lstrin[i].isalnum ():
            normalized += lstrin[i]
            alnumfound = True

    return normalized

def _singleton (x):
    """If we don't know whether getPPDs() or getPPDs2() was used, this
    function can unwrap an item from a list in either case."""
    if isinstance (x, list):
        return x[0]
    return x

class PPDs:
    """
    This class is for handling the list of PPDs returned by CUPS.  It
    indexes by PPD name and device ID, filters by natural language so
    that foreign-language PPDs are not included, and sorts by driver
    type.  If an exactly-matching PPD is not available, it can
    substitute with a PPD for a similar model or for a generic driver.
    """

    # Status of match.
    STATUS_SUCCESS = 0
    STATUS_MODEL_MISMATCH = 1
    STATUS_GENERIC_DRIVER = 2
    STATUS_NO_DRIVER = 3

    FIT_EXACT_CMD = xmldriverprefs.DriverType.FIT_EXACT_CMD
    FIT_EXACT = xmldriverprefs.DriverType.FIT_EXACT
    FIT_CLOSE = xmldriverprefs.DriverType.FIT_CLOSE
    FIT_GENERIC = xmldriverprefs.DriverType.FIT_GENERIC
    FIT_NONE = xmldriverprefs.DriverType.FIT_NONE

    _fit_to_status = { FIT_EXACT_CMD: STATUS_SUCCESS,
                       FIT_EXACT: STATUS_SUCCESS,
                       FIT_CLOSE: STATUS_MODEL_MISMATCH,
                       FIT_GENERIC: STATUS_GENERIC_DRIVER,
                       FIT_NONE: STATUS_NO_DRIVER }

    def __init__ (self, ppds, language=None, xml_dir=None):
        """
        @type ppds: dict
        @param ppds: dict of PPDs as returned by cups.Connection.getPPDs()
        or cups.Connection.getPPDs2()

        @type language: string
	@param language: language name, as given by the first element
        of the pair returned by locale.getlocale()
        """
        self.ppds = ppds.copy ()
        self.makes = None
        self.ids = None

        self.drivertypes = xmldriverprefs.DriverTypes ()
        self.preforder = xmldriverprefs.PreferenceOrder ()
        if xml_dir is None:
            xml_dir = os.environ.get ("CUPSHELPERS_XMLDIR")
            if xml_dir is None:
                from . import config
                xml_dir = os.path.join (config.sysconfdir, "cupshelpers")

        try:
            xmlfile = os.path.join (xml_dir, "preferreddrivers.xml")
            (drivertypes, preferenceorder) = \
                xmldriverprefs.PreferredDrivers (xmlfile)
            self.drivertypes.load (drivertypes)
            self.preforder.load (preferenceorder)
        except Exception as e:
            print("Error loading %s: %s" % (xmlfile, e))
            self.drivertypes = None
            self.preforder = None

        if (language is None or
            language == "C" or
            language == "POSIX"):
            language = "en_US"

        u = language.find ("_")
        if u != -1:
            short_language = language[:u]
        else:
            short_language = language

        to_remove = []
        for ppdname, ppddict in self.ppds.items ():
            try:
                natural_language = _singleton (ppddict['ppd-natural-language'])
            except KeyError:
                continue

            if natural_language == "en":
                # Some manufacturer's PPDs are only available in this
                # language, so always let them though.
                continue

            if natural_language == language:
                continue

            if natural_language == short_language:
                continue

            to_remove.append (ppdname)

        for ppdname in to_remove:
            del self.ppds[ppdname]

        # CUPS sets the 'raw' model's ppd-make-and-model to 'Raw Queue'
        # which unfortunately then appears as manufacturer Raw and
        # model Queue.  Use 'Generic' for this model.
        if 'raw' in self.ppds:
            makemodel = _singleton (self.ppds['raw']['ppd-make-and-model'])
            if not makemodel.startswith ("Generic "):
                self.ppds['raw']['ppd-make-and-model'] = "Generic " + makemodel

    def getMakes (self):
        """
	@returns: a list of strings representing makes, sorted according
        to the current locale
	"""
        self._init_makes ()
        makes_list = list(self.makes.keys ())
        makes_list.sort (key=locale.strxfrm)
        try:
            # "Generic" should be listed first.
            makes_list.remove ("Generic")
            makes_list.insert (0, "Generic")
        except ValueError:
            pass
        return makes_list

    def getModels (self, make):
        """
	@returns: a list of strings representing models, sorted using
	cups.modelSort()
	"""
        self._init_makes ()
        try:
            models_list = list(self.makes[make].keys ())
        except KeyError:
            return []

        def compare_models (a,b):
            first = normalize (a)
            second = normalize (b)
            return cups.modelSort(first, second)
        models_list.sort(key=functools.cmp_to_key(compare_models))
        return models_list

    def getInfoFromModel (self, make, model):
        """
	Obtain a list of PPDs that are suitable for use with a
        particular printer model, given its make and model name.

	@returns: a dict, indexed by ppd-name, of dicts representing
        PPDs (as given by cups.Connection.getPPDs)
	"""
        self._init_makes ()
        try:
            return self.makes[make][model]
        except KeyError:
            return {}

    def getInfoFromPPDName (self, ppdname):
        """
	@returns: a dict representing a PPD, as given by
	cups.Connection.getPPDs
	"""
        return self.ppds[ppdname]

    def getStatusFromFit (self, fit):
        return self._fit_to_status.get (fit, xmldriverprefs.DriverType.FIT_NONE)

    def orderPPDNamesByPreference (self, ppdnamelist=None,
                                   downloadedfiles=None,
                                   make_and_model=None,
                                   devid=None, fit=None):
        """

	Sort a list of PPD names by preferred driver type.

	@param ppdnamelist: PPD names
	@type ppdnamelist: string list
        @param downloadedfiles: Filenames from packages downloaded
        @type downloadedfiles: string list
        @param make_and_model: device-make-and-model name
        @type make_and_model: string
        @param devid: Device ID dict
        @type devid: dict indexed by Device ID field name, of strings;
        except for CMD field which must be a string list
        @param fit: Driver fit string for each PPD name
        @type fit: dict of PPD name:fit
	@returns: string list
	"""
        if ppdnamelist is None:
            ppdnamelist = []

        if downloadedfiles is None:
            downloadedfiles = []

        if fit is None:
            fit = {}

        if self.drivertypes and self.preforder:
            ppds = {}
            for ppdname in ppdnamelist:
                ppds[ppdname] = self.ppds[ppdname]

            orderedtypes = self.preforder.get_ordered_types (self.drivertypes,
                                                             make_and_model,
                                                             devid)
            _debugprint("Valid driver types for this printer in priority order: %s" % repr(orderedtypes))
            orderedppds = self.drivertypes.get_ordered_ppdnames (orderedtypes,
                                                                 ppds, fit)
            _debugprint("PPDs with assigned driver types in priority order: %s" % repr(orderedppds))
            ppdnamelist = [typ_name[1] for typ_name in orderedppds]
            _debugprint("Resulting PPD list in priority order: %s" % repr(ppdnamelist))

        # Special handling for files we've downloaded.  First collect
        # their basenames.
        downloadedfnames = set()
        for downloadedfile in downloadedfiles:
            (path, slash, fname) = downloadedfile.rpartition ("/")
            downloadedfnames.add (fname)

        if downloadedfnames:
            # Next compare the basenames of each ppdname
            downloadedppdnames = []
            for ppdname in ppdnamelist:
                (path, slash, ppdfname) = ppdname.rpartition ("/")
                if ppdfname in downloadedfnames:
                    downloadedppdnames.append (ppdname)

            # Finally, promote the matching ones to the head of the list.
            if downloadedppdnames:
                for ppdname in ppdnamelist:
                    if ppdname not in downloadedppdnames:
                        downloadedppdnames.append (ppdname)

                ppdnamelist = downloadedppdnames

        return ppdnamelist

    def getPPDNamesFromDeviceID (self, mfg, mdl, description="",
                                 commandsets=None, uri=None,
                                 make_and_model=None):
        """
	Obtain a best-effort PPD match for an IEEE 1284 Device ID.

	@param mfg: MFG or MANUFACTURER field
	@type mfg: string
	@param mdl: MDL or MODEL field
	@type mdl: string
	@param description: DES or DESCRIPTION field, optional
	@type description: string
	@param commandsets: CMD or COMMANDSET field, optional
	@type commandsets: string
	@param uri: device URI, optional (only needed for debugging)
	@type uri: string
        @param make_and_model: device-make-and-model string
        @type make_and_model: string
	@returns: a dict of fit (string) indexed by PPD name
	"""
        _debugprint ("\n%s %s" % (mfg, mdl))
        orig_mfg = mfg
        orig_mdl = mdl
        self._init_ids ()

        if commandsets is None:
            commandsets = []

        # Start with an empty result list and build it up using
        # several search methods, in increasing order of fuzziness.
        fit = {}

        # First, try looking up the device using the manufacturer and
        # model fields from the Device ID exactly as they appear (but
        # case-insensitively).
        mfgl = mfg.lower ()
        mdll = mdl.lower ()

        id_matched = False
        try:
            for each in self.ids[mfgl][mdll]:
                fit[each] = self.FIT_EXACT
            id_matched = True
        except KeyError:
            pass

        # The HP PPDs say "HP" not "Hewlett-Packard", so try that.
        if mfgl == "hewlett-packard":
            try:
                for each in self.ids["hp"][mdll]:
                    fit[each] = self.FIT_EXACT
                _debugprint ("**** Incorrect IEEE 1284 Device ID: %s" %
                             self.ids["hp"][mdll])
                _debugprint ("**** Actual ID is MFG:%s;MDL:%s;" % (mfg, mdl))
                _debugprint ("**** Please report a bug against the HPLIP component")
                id_matched = True
            except KeyError:
                pass

        # Now try looking up the device by ppd-make-and-model.
        _debugprint ("Trying make/model names")
        mdls = None
        self._init_makes ()
        make = None
        if mfgl == "":
            (mfg, mdl) = ppdMakeModelSplit (mdl)
            mfgl = normalize (mfg)
            mdll = normalize (mdl)

        _debugprint ("mfgl: %s" % mfgl)
        _debugprint ("mdll: %s" % mdll)
        mfgrepl = {"hewlett-packard": "hp",
                   "lexmark international": "lexmark",
                   "kyocera": "kyocera mita"}
        if mfgl in self.lmakes:
            # Found manufacturer.
            make = self.lmakes[mfgl]
        elif mfgl in mfgrepl:
            rmfg = mfgrepl[mfgl]
            if rmfg in self.lmakes:
                mfg = rmfg
                mfgl = mfg
                # Found manufacturer (after mapping to canonical name)
                _debugprint ("remapped mfgl: %s" % mfgl)
                make = self.lmakes[mfgl]

        _debugprint ("make: %s" % make)
        if make is not None:
            mdls = self.makes[make]
            mdlsl = self.lmodels[normalize(make)]

            # Remove manufacturer name from model field
            for prefix in [mfgl, 'hewlett-packard', 'hp']:
                if mdll.startswith (prefix + ' '):
                    mdl = mdl[len (prefix) + 1:]
                    mdll = normalize (mdl)
                    _debugprint ("unprefixed mdll: %s" % mdll)

            if mdll in self.lmodels[mfgl]:
                model = mdlsl[mdll]
                for each in mdls[model].keys ():
                    fit[each] = self.FIT_EXACT
                    _debugprint ("%s: %s" % (fit[each], each))
            else:
                # Make use of the model name clean-up in the
                # ppdMakeModelSplit () function
                (mfg2, mdl2) = ppdMakeModelSplit (mfg + " " + mdl)
                mdl2l = normalize (mdl2)
                _debugprint ("re-split mdll: %s" % mdl2l)
                if mdl2l in self.lmodels[mfgl]:
                    model = mdlsl[mdl2l]
                    for each in list(mdls[model].keys ()):
                        fit[each] = self.FIT_EXACT
                        _debugprint ("%s: %s" % (fit[each], each))
      
        if not fit and mdls:
            (s, ppds) = self._findBestMatchPPDs (mdls, mdl)
            if s != self.FIT_NONE:
                for each in ppds:
                    fit[each] = s
                    _debugprint ("%s: %s" % (fit[each], each))

        if commandsets:
            if type (commandsets) != list:
                commandsets = commandsets.split (',')

            _debugprint ("Checking CMD field")
            generic = self._getPPDNameFromCommandSet (commandsets)
            if generic:
                for driver in generic:
                    fit[driver] = self.FIT_GENERIC
                    _debugprint ("%s: %s" % (fit[driver], driver))

        # Check by the URI whether our printer is connected via IPP
        # and if not, remove the PPD entries for driverless printing
        # (ppdname = "driverless:..." from the list)
        if (not uri or
            (not uri.startswith("ipp:") and
             not uri.startswith("ipps:") and
             (not uri.startswith("dnssd") or
              not "._ipp" in uri))):
            failed = set()
            for ppdname in fit.keys ():
                if (ppdname.startswith("driverless:")):
                    failed.add (ppdname)
            if (len(failed) > 0):
                _debugprint ("Removed %s due to non-IPP connection" % failed)
                for each in failed:
                    del fit[each]
            failed = set()

        # What about the CMD field of the Device ID?  Some devices
        # have optional units for page description languages, such as
        # PostScript, and they will report different CMD strings
        # accordingly.
        #
        # By convention, if a PPD contains a Device ID with a CMD
        # field, that PPD can only be used whenever any of the
        # comma-separated words in the CMD field appear in the
        # device's ID.
        # (See Red Hat bug #630058).
        #
        # We'll do that check now, and any PPDs that fail
        # (e.g. PostScript PPD for non-PostScript printer) can be
        # eliminated from the list.
        #
        # The reason we don't do this check any earlier is that we
        # don't want to eliminate PPDs only to have the fuzzy matcher
        # add them back in afterwards.
        #
        # While doing this, any drivers that we can positively confirm
        # as using a command set understood by the printer will be
        # converted from FIT_EXACT to FIT_EXACT_CMD.
        if id_matched and len (commandsets) > 0:
            failed = set()
            exact_cmd = set()
            for ppdname in fit.keys ():
                ppd_cmd_field = None
                ppd = self.ppds[ppdname]
                ppd_device_id = _singleton (ppd.get ('ppd-device-id'))
                if ppd_device_id:
                    ppd_device_id_dict = parseDeviceID (ppd_device_id)
                    ppd_cmd_field = ppd_device_id_dict["CMD"]

                if (not ppd_cmd_field and
                    # ppd-type is not reliable for driver-generated
                    # PPDs (see CUPS STR #3720).  Neither gutenprint
                    # nor foomatic specify ppd-type in their CUPS
                    # drivers.
                    ppdname.find (":") == -1):
                    # If this is a PostScript PPD we know which
                    # command set it will use.
                    ppd_type = _singleton (ppd.get ('ppd-type'))
                    if ppd_type == "postscript":
                        ppd_cmd_field = ["POSTSCRIPT"]

                if not ppd_cmd_field:
                    # We can't be sure which command set this driver
                    # uses.
                    continue

                usable = False
                for pdl in ppd_cmd_field:
                    if pdl in commandsets:
                        usable = True
                        break

                if usable:
                    exact_cmd.add (ppdname)
                else:
                    failed.add (ppdname)

            # Assign the more specific fit "exact-cmd" to those that
            # positively matched the CMD field.
            for each in exact_cmd:
                if fit[each] == self.FIT_EXACT:
                    fit[each] = self.FIT_EXACT_CMD
                    _debugprint (self.FIT_EXACT_CMD + ": %s" % each)

            if len (failed) < len ([d for (d, m) in fit.items ()
                                    if m != 'generic']):
                _debugprint ("Removed %s due to CMD mis-match" % failed)
                for each in failed:
                    del fit[each]
            else:
                _debugprint ("Not removing %s " % failed +
                             "due to CMD mis-match as it would "
                             "leave nothing good")

        if not fit:
            fallbacks = ["textonly.ppd", "postscript.ppd"]
            found = False
            for fallback in fallbacks:
                _debugprint ("'%s' fallback" % fallback)
                fallbackgz = fallback + ".gz"
                for ppdpath in self.ppds.keys ():
                    if (ppdpath.endswith (fallback) or
                        ppdpath.endswith (fallbackgz)):
                        fit[ppdpath] = self.FIT_NONE
                        found = True
                        break

                if found:
                    break

                _debugprint ("Fallback '%s' not available" % fallback)

            if not found:
                _debugprint ("No fallback available; choosing any")
                fit[list(self.ppds.keys ())[0]] = self.FIT_NONE

        if not id_matched:
            sanitised_uri = re.sub (pattern="//[^@]*@/?", repl="//",
                                    string=str (uri))
            try:
                cmd = reduce (lambda x, y: x + ","+ y, commandsets)
            except TypeError:
                cmd = ""
            id = "MFG:%s;MDL:%s;" % (orig_mfg, orig_mdl)
            if cmd:
                id += "CMD:%s;" % cmd
            if description:
                id += "DES:%s;" % description

            _debugprint ("No ID match for device %s:" % sanitised_uri)
            _debugprint (id)

        return fit

    def getPPDNameFromDeviceID (self, mfg, mdl, description="",
                                commandsets=None, uri=None,
                                downloadedfiles=None,
                                make_and_model=None):
        """
	Obtain a best-effort PPD match for an IEEE 1284 Device ID.
	The status is one of:

	  - L{STATUS_SUCCESS}: the match was successful, and an exact
            match was found

	  - L{STATUS_MODEL_MISMATCH}: a similar match was found, but
            the model name does not exactly match

	  - L{STATUS_GENERIC_DRIVER}: no match was found, but a
            generic driver is available that can drive this device
            according to its command set list

	  - L{STATUS_NO_DRIVER}: no match was found at all, and the
            returned PPD name is a last resort

	@param mfg: MFG or MANUFACTURER field
	@type mfg: string
	@param mdl: MDL or MODEL field
	@type mdl: string
	@param description: DES or DESCRIPTION field, optional
	@type description: string
	@param commandsets: CMD or COMMANDSET field, optional
	@type commandsets: string
	@param uri: device URI, optional (only needed for debugging)
	@type uri: string
        @param downloadedfiles: filenames from downloaded packages
        @type downloadedfiles: string list
        @param make_and_model: device-make-and-model string
        @type make_and_model: string
	@returns: an integer,string pair of (status,ppd-name)
	"""

        if commandsets is None:
            commandsets = []

        if downloadedfiles is None:
            downloadedfiles = []

        fit = self.getPPDNamesFromDeviceID (mfg, mdl, description,
                                            commandsets, uri,
                                            make_and_model)

        # We've got a set of PPDs, any of which will drive the device.
        # Now we have to choose the "best" one.  This is quite tricky
        # to decide, so let's sort them in order of preference and
        # take the first.
        devid = { "MFG": mfg, "MDL": mdl,
                  "DES": description,
                  "CMD": commandsets }
        ppdnamelist = self.orderPPDNamesByPreference (list(fit.keys ()),
                                                      downloadedfiles,
                                                      make_and_model,
                                                      devid, fit)
        _debugprint ("Found PPDs: %s" % str (ppdnamelist))

        status = self.getStatusFromFit (fit[ppdnamelist[0]])
        _debugprint ("Using %s (status: %d)" % (ppdnamelist[0], status))
        return (status, ppdnamelist[0])

    def _findBestMatchPPDs (self, mdls, mdl):
        """
        Find the best-matching PPDs based on the MDL Device ID.
        This function could be made a lot smarter.
        """

        _debugprint ("Trying best match")
        mdll = mdl.lower ()
        if mdll.endswith (" series"):
            # Strip " series" from the end of the MDL field.
            mdll = mdll[:-7]
            mdl = mdl[:-7]
        best_mdl = None
        best_matchlen = 0
        mdlnames = list(mdls.keys ())

        # Perform a case-insensitive model sort on the names.
        mdlnamesl = [(x, x.lower()) for x in mdlnames]
        mdlnamesl.append ((mdl, mdll))
        mdlnamesl.sort (key=functools.cmp_to_key(lambda x, y: cups.modelSort(x[1], y[1])))
        i = mdlnamesl.index ((mdl, mdll))
        candidates = [mdlnamesl[i - 1]]
        if i + 1 < len (mdlnamesl):
            candidates.append (mdlnamesl[i + 1])
            _debugprint (candidates[0][0] + " <= " + mdl + " <= " +
                        candidates[1][0])
        else:
            _debugprint (candidates[0][0] + " <= " + mdl)

        # Look at the models immediately before and after ours in the
        # sorted list, and pick the one with the longest initial match.
        for (candidate, candidatel) in candidates:
            prefix = os.path.commonprefix ([candidatel, mdll])
            if len (prefix) > best_matchlen:
                best_mdl = list(mdls[candidate].keys ())
                best_matchlen = len (prefix)
                _debugprint ("%s: match length %d" % (candidate, best_matchlen))

        # Did we match more than half of the model name?
        if best_mdl and best_matchlen > (len (mdll) / 2):
            ppdnamelist = best_mdl
            if best_matchlen == len (mdll):
                fit = self.FIT_EXACT
            else:
                fit = self.FIT_CLOSE
        else:
            fit = self.FIT_NONE
            ppdnamelist = None

            # Last resort.  Find the "most important" word in the MDL
            # field and look for a match based solely on that.  If
            # there are digits, try lowering the number of
            # significant figures.
            mdlnames.sort (key=functools.cmp_to_key(cups.modelSort))
            mdlitems = [(x.lower (), mdls[x]) for x in mdlnames]
            modelid = None
            for word in mdll.split (' '):
                if modelid is None:
                    modelid = word

                have_digits = False
                for i in range (len (word)):
                    if word[i].isdigit ():
                        have_digits = True
                        break

                if have_digits:
                    modelid = word
                    break

            digits = 0
            digits_start = -1
            digits_end = -1
            for i in range (len (modelid)):
                if modelid[i].isdigit ():
                    if digits_start == -1:
                        digits_start = i
                    digits_end = i
                    digits += 1
                elif digits_start != -1:
                    break
            digits_end += 1
            modelnumber = 0
            if digits > 0:
                modelnumber = int (modelid[digits_start:digits_end])
                modelpattern = (modelid[:digits_start] + "%d" +
                                modelid[digits_end:])
                _debugprint ("Searching for model ID '%s', '%s' %% %d" %
                             (modelid, modelpattern, modelnumber))
                ignore_digits = 0
                best_mdl = None
                found = False
                while ignore_digits < digits:
                    div = pow (10, ignore_digits)
                    modelid = modelpattern % ((modelnumber / div) * div)
                    _debugprint ("Ignoring %d of %d digits, trying %s" %
                                 (ignore_digits, digits, modelid))

                    for (name, ppds) in mdlitems:
                        for word in name.split (' '):
                            if word.lower () == modelid:
                                found = True
                                break

                        if found:
                            best_mdl = list(ppds.keys ())
                            break

                    if found:
                        break

                    ignore_digits += 1
                    if digits < 2:
                        break

                if found:
                    ppdnamelist = best_mdl
                    fit = self.FIT_CLOSE

        return (fit, ppdnamelist)

    def _getPPDNameFromCommandSet (self, commandsets=None):
        """Return ppd-name list or None, given a list of strings representing
        the command sets supported."""

        if commandsets is None:
            commandsets = []

        try:
            self._init_makes ()
            models = self.makes["Generic"]
        except KeyError:
            return None

        def get (*candidates):
            for model in candidates:
                (s, ppds) = self._findBestMatchPPDs (models, model)
                if s == self.FIT_EXACT:
                    return ppds
            return None

        cmdsets = [x.lower () for x in commandsets]
        if (("postscript" in cmdsets) or ("postscript2" in cmdsets) or
            ("postscript level 2 emulation" in cmdsets)):
            return get ("PostScript")
        elif (("pclxl" in cmdsets) or ("pcl-xl" in cmdsets) or
              ("pcl6" in cmdsets) or ("pcl 6 emulation" in cmdsets)):
            return get ("PCL 6/PCL XL", "PCL Laser")
        elif "pcl5e" in cmdsets:
            return get ("PCL 5e", "PCL Laser")
        elif "pcl5c" in cmdsets:
            return get ("PCL 5c", "PCL Laser")
        elif ("pcl5" in cmdsets) or ("pcl 5 emulation" in cmdsets):
            return get ("PCL 5", "PCL Laser")
        elif "pcl" in cmdsets:
            return get ("PCL 3", "PCL Laser")
        elif (("escpl2" in cmdsets) or ("esc/p2" in cmdsets) or
              ("escp2e" in cmdsets)):
            return get ("ESC/P Dot Matrix")
        return None

    def _init_makes (self):
        if self.makes:
            return

        tstart = time.time ()
        makes = {}
        lmakes = {}
        lmodels = {}
        aliases = {} # Generic model name: set(specific model names)
        for ppdname, ppddict in self.ppds.items ():
            # One entry for ppd-make-and-model
            ppd_make_and_model = _singleton (ppddict['ppd-make-and-model'])
            ppd_mm_split = ppdMakeModelSplit (ppd_make_and_model)
            ppd_makes_and_models = set([ppd_mm_split])

            # The ppd-product IPP attribute contains values from each
            # Product PPD attribute as well as the value from the
            # ModelName attribute if present.  The Product attribute
            # values are surrounded by parentheses; the ModelName
            # attribute value is not.

            # Add another entry for each ppd-product that came from a
            # Product attribute in the PPD file.
            ppd_products = ppddict.get ('ppd-product', [])
            if not isinstance (ppd_products, list):
                ppd_products = [ppd_products]
            ppd_products = set ([x for x in ppd_products if x.startswith ("(")])
            if ppd_products:
                # If there is only one ppd-product value it is
                # unlikely to be useful.
                if len (ppd_products) == 1:
                    ppd_products = set()

                make = _singleton (ppddict.get ('ppd-make', '')).rstrip ()
                if make:
                    make += ' '
                lmake = normalize (make)
                for ppd_product in ppd_products:
                    # *Product: attribute is "(text)"
                    if (ppd_product.startswith ("(") and
                        ppd_product.endswith (")")):
                        ppd_product = ppd_product[1:len (ppd_product) - 1]

                    if not ppd_product:
                        continue

                    # If manufacturer name missing, take it from ppd-make
                    lprod = normalize (ppd_product)
                    if not lprod.startswith (lmake):
                        ppd_product = make + ppd_product

                    ppd_makes_and_models.add (ppdMakeModelSplit (ppd_product))

            # Add the entries to our dictionary
            for make, model in ppd_makes_and_models:
                lmake = normalize (make)
                lmodel = normalize (model)
                if lmake not in lmakes:
                    lmakes[lmake] = make
                    lmodels[lmake] = {}
                    makes[make] = {}
                else:
                    make = lmakes[lmake]

                if lmodel not in lmodels[lmake]:
                    lmodels[lmake][lmodel] = model
                    makes[make][model] = {}
                else:
                    model = lmodels[lmake][lmodel]

                makes[make][model][ppdname] = ppddict

            # Build list of model aliases
            if ppd_mm_split in ppd_makes_and_models:
                ppd_makes_and_models.remove (ppd_mm_split)

            if ppd_makes_and_models:
                (make, model) = ppd_mm_split
                if make in aliases:
                    models = aliases[make].get (model, set())
                else:
                    aliases[make] = {}
                    models = set()

                models = models.union ([x[1] for x in ppd_makes_and_models])
                aliases[make][model] = models

        # Now, for each set of model aliases, add all drivers from the
        # "main" (generic) model name to each of the specific models.
        for make, models in aliases.items ():
            lmake = normalize (make)
            main_make = lmakes[lmake]
            for model, modelnames in models.items ():
                main_model = lmodels[lmake].get (normalize (model))
                if not main_model:
                    continue

                main_ppds = makes[main_make][main_model]

                for eachmodel in modelnames:
                    this_model = lmodels[lmake].get (normalize (eachmodel))
                    ppds = makes[main_make][this_model]
                    ppds.update (main_ppds)

        self.makes = makes
        self.lmakes = lmakes
        self.lmodels = lmodels
        _debugprint ("init_makes: %.3fs" % (time.time () - tstart))

    def _init_ids (self):
        if self.ids:
            return

        ids = {}
        for ppdname, ppddict in self.ppds.items ():
            id = _singleton (ppddict.get ('ppd-device-id'))
            if not id:
                continue

            id_dict = parseDeviceID (id)
            lmfg = id_dict['MFG'].lower ()
            lmdl = id_dict['MDL'].lower ()

            bad = False
            if len (lmfg) == 0:
                bad = True
            if len (lmdl) == 0:
                bad = True
            if bad:
                continue

            if lmfg not in ids:
                ids[lmfg] = {}

            if lmdl not in ids[lmfg]:
                ids[lmfg][lmdl] = []

            ids[lmfg][lmdl].append (ppdname)

        self.ids = ids

def _show_help():
    print ("usage: ppds.py [--deviceid] [--list-models] [--list-ids] [--debug]")

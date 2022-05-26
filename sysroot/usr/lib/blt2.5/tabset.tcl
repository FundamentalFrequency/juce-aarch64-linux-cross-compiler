#
# tabset.tcl
#
# ----------------------------------------------------------------------
# Bindings for the BLT tabset widget
# ----------------------------------------------------------------------
#   AUTHOR:  George Howlett
#            Bell Labs Innovations for Lucent Technologies
#            gah@bell-labs.com
#            http://www.tcltk.com/blt
# ----------------------------------------------------------------------
# Copyright (c) 1998  Lucent Technologies, Inc.
# ======================================================================
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that the copyright notice and warranty disclaimer appear in
# supporting documentation, and that the names of Lucent Technologies
# any of their entities not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# Lucent Technologies disclaims all warranties with regard to this
# software, including all implied warranties of merchantability and
# fitness.  In no event shall Lucent be liable for any special, indirect
# or consequential damages or any damages whatsoever resulting from loss
# of use, data or profits, whether in an action of contract, negligence
# or other tortuous action, arising out of or in connection with the use
# or performance of this software.
#
# ======================================================================

#
# Indicates whether to activate (highlight) tabs when the mouse passes
# over them.  This is turned off during scan operations.
#
namespace eval ::blt {
  variable bltTabset
  set bltTabset(activate) yes
  set bltTabset(insel) 0
}

# ----------------------------------------------------------------------
# 
# ButtonPress assignments
#
#   <ButtonPress-2>	Starts scan mechanism (pushes the tabs)
#   <B2-Motion>		Adjust scan
#   <ButtonRelease-2>	Stops scan
#
# ----------------------------------------------------------------------
bind Tabset <B2-Motion> {
    %W scan dragto %x %y
}

bind Tabset <ButtonPress-2> {
    set ::blt::bltTabset(cursor) [%W cget -cursor]
    set ::blt::bltTabset(activate) no
    %W configure -cursor hand1
    %W scan mark %x %y
}

bind Tabset <ButtonRelease-2> {
    %W configure -cursor $::blt::bltTabset(cursor)
    set ::blt::bltTabset(activate) yes
    catch { %W activate @%x,%y }
}

# ----------------------------------------------------------------------
# 
# KeyPress assignments
#
#   <KeyPress-Up>	Moves focus to the tab immediately above the 
#			current.
#   <KeyPress-Down>	Moves focus to the tab immediately below the 
#			current.
#   <KeyPress-Left>	Moves focus to the tab immediately left of the 
#			currently focused tab.
#   <KeyPress-Right>	Moves focus to the tab immediately right of the 
#			currently focused tab.
#   <KeyPress-space>	Invokes the commands associated with the current
#			tab.
#   <KeyPress-Return>	Same as above.
#   <KeyPress>		Go to next tab starting with the ASCII character.
#
# ----------------------------------------------------------------------
bind Tabset <KeyPress-Up> { blt::TabsetSelect %W "up" }
bind Tabset <KeyPress-Down> { blt::TabsetSelect %W "down" }
bind Tabset <KeyPress-Right> { blt::TabsetSelect %W "right" }
bind Tabset <KeyPress-Left> { blt::TabsetSelect %W "left" }
bind Tabset <KeyPress-Next> { blt::TabsetSelect %W "next" }
bind Tabset <KeyPress-Prior> { blt::TabsetSelect %W "prev" }
bind Tabset <KeyPress-Home> { blt::TabsetSelect %W "begin" }
bind Tabset <KeyPress-End> { blt::TabsetSelect %W "end" }
bind Tabset <KeyPress-space> { %W invoke focus }
bind Tabset <KeyPress-Return> { blt::TabsetSelect %W focus }

bind Tabset <KeyPress> { blt::TabsetAccel %W %A }

# ----------------------------------------------------------------------
#
# TabsetAccel --
#
#	Find the first tab (from the tab that currently has focus) 
#	starting with the same first letter as the tab.  It searches
#	in order of the tab positions and wraps around. If no tab
#	matches, it stops back at the current tab.
#
# Arguments:	
#	widget		Tabset widget.
#	key		ASCII character of key pressed
#
# ----------------------------------------------------------------------
proc blt::TabsetAccel { widget key } {
    if {$key == "" || ![string is print $key]} return
    set key [string tolower $key]
    set itab [$widget index focus]
    set numTabs [$widget size]
    for { set i 0 } { $i < $numTabs } { incr i } {
	if { [incr itab] >= $numTabs } {
	    set itab 0
	}
	set ul [$widget tab cget $itab -underline]
	set name [$widget get $itab]
	set label [string tolower [$widget tab cget $name -text]]
	if { [string index $label $ul] == $key } {
	    break
	}
    }
    TabsetSelect $widget $itab
}

proc blt::TabsetRaise { widget } {
     wm withdraw $widget
     wm deiconify $widget
     raise $widget
}

# ----------------------------------------------------------------------
#
# TabsetSelect --
#
#	Invokes the command for the tab.  If the widget associated tab 
#	is currently torn off, the tearoff is raised.
#
# Arguments:	
#	widget		Tabset widget.
#	x y		Unused.
#
# ----------------------------------------------------------------------
proc blt::TabsetSelect { widget tab } {
    variable bltTabset
    if {$bltTabset(insel)} return
    set rc [catch {
       set bltTabset(insel) 1
   
       set index [$widget index -both $tab]
       if { $index != "" } {
           if {[$widget index select] == $index} {
	       $widget see $index
           } else {
               focus $widget
               $widget activate $index
	       $widget select $index
	       $widget focus $index
	       $widget see $index
	       set torn [$widget tab cget $index -tornwindow]
	       if {$torn != {}} {
                    raise $torn
               }
	       $widget invoke $index
               event generate $widget <<TabsetSelect>>
           }
       }
       set rv ""
    } rv]
    set bltTabset(insel) 0
    return -code $rc $rv
}

proc blt::DestroyTearoff { widget tab window} {
    wm forget $window
    $widget tab conf $tab -tornwindow {}
    event generate $widget <<TabsetUntearoff>> -x [$widget tab number $tab]
    $widget tab conf $tab -window $window
}

proc blt::CreateTearoff { widget tab args } {

    # ------------------------------------------------------------------
    # When reparenting the window contained in the tab, check if the
    # window or any window in its hierarchy currently has focus.
    # Since we're reparenting windows behind its back, Tk can
    # mistakenly activate the keyboard focus when the mouse enters the
    # old toplevel.  The simplest way to deal with this problem is to
    # take the focus off the window and set it to the tabset widget
    # itself.
    # ------------------------------------------------------------------

    set tab [$widget index $tab]
    set focus [focus]
    set name [$widget get $tab]
    set window [$widget tab cget $name -window]
    if { ($focus == $window) || ([string match  $window.* $focus]) } {
        focus -force $widget
    }
    if {$window == {}} return
    wm manage $window
    wm title $window "[$widget tab cget $name -text]"
    if {[winfo width $widget]>10} {
        wm geometry $window [winfo width $widget]x[winfo height $widget]
    }
    $widget tab conf $tab -tornwindow $window
    # If the user tries to delete the toplevel, put the window back
    # into the tab folder.  
    wm protocol $window WM_DELETE_WINDOW [list blt::DestroyTearoff $widget $tab $window]
    event generate $widget <<TabsetTearoff>> -x [$widget tab number $tab]
}

# ----------------------------------------------------------------------
#
# Tearoff --
#
#	Toggles the tab tearoff.  If the tab contains a embedded widget, 
#	it is placed inside of a toplevel window.  If the widget has 
#	already been torn off, the widget is replaced back in the tab.
#
# Arguments:	
#	widget		tabset widget.
#	x y		The coordinates of the mouse pointer.
#
# ----------------------------------------------------------------------
proc blt::Tearoff { widget x y index } {
    set tab [$widget index -index $index]
    if { $tab == "" } {
	return
    }
    $widget invoke $tab

    set torn [$widget tab tearoff $index]
    if { $torn == $widget } {
	blt::CreateTearoff $widget $tab $x $y
    } else {
        set window [$widget tab cget $tab -window]
	blt::DestroyTearoff $widget $tab $window
    }
}

proc blt::TabsetTearoff { widget {index focus} } {
    set tab [$widget index -both $index]
    if { $tab == "" } {
        return
    }
    $widget invoke $tab

    set window [$widget tab cget $tab -window]
    if { $window != {}} {
        blt::CreateTearoff $widget $tab 
    } else {
        set window [$widget tab cget $tab -tornwindow]
        blt::DestroyTearoff $widget $tab $window
    }
}

# ----------------------------------------------------------------------
#
# TabsetInit
#
#	Invoked from C whenever a new tabset widget is created.
#	Sets up the default bindings for the all tab entries.  
#	These bindings are local to the widget, so they can't be 
#	set through the usual widget class bind tags mechanism.
#
#	<Enter>		Activates the tab.
#	<Leave>		Deactivates all tabs.
#	<ButtonPress-1>	Selects the tab and invokes its command.
#	<Control-ButtonPress-1>	
#			Toggles the tab tearoff.  If the tab contains
#			a embedded widget, it is placed inside of a
#			toplevel window.  If the widget has already
#			been torn off, the widget is replaced back
#			in the tab.
#
# Arguments:	
#	widget		tabset widget
#
# ----------------------------------------------------------------------
proc blt::TabsetInit { widget } {
    $widget bind all <Enter> { 
	if { $::blt::bltTabset(activate) } {
	    %W activate current
        }
    }
    $widget bind all <Leave> { 
        %W activate "" 
    }
    $widget bind all <ButtonPress-1> { 
	blt::TabsetSelect %W "current"
    }
    $widget bind all <Control-ButtonPress-1> { 
	if { [%W cget -tearoff] } {
	    blt::Tearoff %W %X %Y active
	}
    }
    $widget configure -perforationcommand {
	blt::Tearoff %W $::blt::bltTabset(x) $::blt::bltTabset(y) select
    }
    $widget bind Perforation <Enter> { 
	%W perforation activate on
    }
    $widget bind Perforation <Leave> { 
	%W perforation activate off
    }
    $widget bind Perforation <ButtonRelease-1> { 
	set ::blt::bltTabset(x) %X
	set ::blt::bltTabset(y) %Y
	%W perforation invoke
    }
}

# Insert a table
proc blt::InsertTable {widget list args} {
   array set p { -colprefix F -colnames {} -conf {} }
   array set p $args
   set w $widget
   foreach cn $p(-colnames) {
       $w column insert end $cn -justify left -bd 1 -relief raised
   }
   set clst [$w column names]
   eval $w conf $p(-conf)
   $w column conf 0 -hide 1
   foreach i $list {
      while {[llength $clst] <= [llength $i]} {
         set cn $p(-colprefix)[llength $clst]
         $w column insert end $cn -justify left -bd 1 -relief raised
         set clst [$w column names]
      }
      set n 0
      set d {}
      foreach j $i {
         incr n
         lappend d [lindex $clst $n] $j
      }
      $w insert end #auto -data $d
   }
}



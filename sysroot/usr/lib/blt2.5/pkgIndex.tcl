# Tcl package index file, version 1.0

proc LoadBLT25 { version dir } {

    set prefix "lib"
    set suffix [info sharedlibextension]
    regsub {\.} $version {} version_no_dots
    set versuf $version$suffix

    # Determine whether to load the full BLT library or
    # the "lite" tcl-only version.
    
   if {[package vcompare [info tclversion] 8.2] < 0} {
        set taillib ${versuf}.8.0
    } elseif {[package vcompare [info tclversion] 8.3] < 0} {
        set taillib ${versuf}.8.2
    } elseif {[package vcompare [info tclversion] 8.4] < 0} {
        set taillib ${versuf}.8.3
    } elseif {[package vcompare [info tclversion] 8.5] < 0} {
        set taillib ${versuf}.8.4
    } elseif {[package vcompare [info tclversion] 8.6] < 0} {
        set taillib ${versuf}.8.5
    } else {
        set taillib ${versuf}.8.6
    }

    if { [info commands tk] == "tk" } {
        set name1 ${prefix}BLT.${taillib}
        set name2 ${prefix}BLT${version_no_dots}${suffix}
    } else {
        set name1 ${prefix}BLTlite.${taillib}
        set name2 ${prefix}BLTlite${version_no_dots}${suffix}
    }
    
    global tcl_platform
    foreach name [list $name1 $name2] {
        if { $tcl_platform(platform) == "unix" } {
	    set library [file join $dir $name]
	    if { ![file exists $library] } {
	        # Try the parent directory.
	        set library [file join [file dirname $dir] $name]
	    }
	    if { ![file exists $library] } {
	        # Default to the path generated at compilation.
	        set library [file join "/usr/lib" $name]
	    }
        } else {
	    set library $name
        }
	if { ![file exists $library] } continue
        load $library BLT
	break
    }
}

set version "2.5"
set patchlevel "2.5.3"

package ifneeded BLT $patchlevel [list LoadBLT25 $version $dir]

# End of package index file

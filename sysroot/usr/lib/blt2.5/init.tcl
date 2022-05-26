namespace eval ::blt {

    proc initializeLibrary {} {
        foreach w {Button Checkbutton Radiobutton Menubutton Label Scrollbar} {
           foreach i [bind $w] {
               bind B$w $i [bind $w $i]
           }
        }
    }

    if {[info commands tk] == "tk"} {
	initializeLibrary
    }
    
}


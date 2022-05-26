# BLT TreeView Utilities.
# Load and dump treeview to XTL form.

namespace eval ::blt::tv {
  variable pc
  set pc(colors) {LightBlue Aquamarine Khaki LightCyan Cornsilk LightYellow Lavender Azure}
}

proc ::blt::tv::_TreeLoad {w tl {id 0}} {
    upvar 1 p p
    foreach {i j} $tl {
        set tag [lindex $i 0]
        if {[llength $i]==1} {
            set lbl [expr {$j == {}?$i:$j}]
            if {$j == {}} {
                $w insert end $tag -at $id
            } else {
                $w insert end $tag -at $id -data [list $p(-datacol) $j]
            }
        } else {
            set tind [lindex $i 1]
            array unset data
            foreach {k l} [lrange $i 2 end] {
                if {$p(-trim) != {}} { set k [string trimleft $k $p(-trim)] }
                set data($k) $l
            }
            set cns [$w col names]
            foreach k [array names data] {
                if {[lsearch -exact $cns $k]<0} {
                    $w col insert end $k
                    foreach m {-relief -bd} { $w col conf $k $m [$w col cget 0 $m] }
                }
            }
            if {$tind != "+"} {
                set data($p(-datacol)) $j
            }
            set nid [$w insert end $tag -at $id -data [array get data]]
            switch -- $tind {
                + {
                    if {$p(-defer)} {
                        $w entry conf $nid -forcetree 1 -opencommand [concat [list ::blt::tv::TreeLoad $w $j] [array get p] -id $nid -nice 0]
                    } else {
                        _TreeLoad $w $j $nid
                    }
                }
                - - {} {}
                default {
                    tclLog "Tag '$tind' is not '+' or '-' in: $i $j"
                }
            }
        }
    }
}

proc ::blt::tv::TreeLoad {w tl args} { #TYPES: . Win . {opts -trim -nice -defer -id -datacol}
    # Load treeview from an XTL.
    array set p {-trim {} -nice 0 -defer 1 -id 0 -datacol Value}
    array set p $args
    if {$p(-id) && [$w entry children $p(-id)] != {}} return
    if {[lsearch -exact [$w col names] $p(-datacol)]<0} {
      $w col insert end $p(-datacol)
    }
    $w conf -allowduplicates 1
    busy hold $w
    update
    set rc [catch {_TreeLoad $w $tl $p(-id)} rv]
    busy release $w
    update
    if {$p(-nice)} {
        $w style create textbox alt -bg LightBlue
        $w conf -underline 1 -altstyle alt -bg White -selectbackground SteelBlue -nofocusselectbackground SteelBlue
        eval $w col conf [$w col names] -bd 1 -relief raised
    }
    return -code $rc $rv
}

proc ::blt::tv::_TreeDump1 {w node} {
    upvar 1 p p rc rc
    set val {}
    set i $node
    if {$p(-label)} {
       set tag [$w entry cget $i -label]
    } else {
       set tag [$w get $i]
    }
    set avals {}
    if {$p(-aval) != {}} {
       catch { set avals [$w entry set $i $p(-aval)] }
    } else {
       set avals [$w entry cget $i -data]
    }
    foreach {j k} $avals {
	if {$j == "#0"} {
	    set val $k
	} else {
	    set j $p(-prefix)$j
	    set data($j) $k
	}
    }
    if {$p(-vval) != {}} {
       catch { set val [$w entry set $i $p(-vval)] }
    }
    if {[$w entry isleaf $i]} {
	if {[array size data]} {
	    set tattr [concat [list $tag -] [array get data]]
	} elseif {[string match #* $tag]} {
	    set tattr $tag
	} else {
	    set tattr [list $tag]
	}
	lappend rc $tattr $val
    } else {
	set tattr [concat [list $tag +] [array get data]]
	lappend rc $tattr [_TreeDump $w $i]
    }
}

proc ::blt::tv::_TreeDump {w node} {
    upvar 1 p p
    set rc {}
    foreach i [$w entry children $node] {
         _TreeDump1 $w $i
    }
    return $rc
}

proc ::blt::tv::FmtTree {lst {ind "    "} {sp {}}} {
    set rc {}
    set n 0
    foreach {atag val} $lst {
        incr n
        if {[string index $rc end] != "\n"} { append rc \n }
        if {[lindex $atag 1] == "+"} {
            set src [FmtTree $val $ind "$sp$ind"]
            append rc $sp [list $atag $src] \n
        } else {
            append rc $sp [list $atag $val] \n
        }
    }
    return $rc[string range $sp 0 end-[string length $ind]]
}

proc ::blt::tv::TreeDump {w args} { #TYPES: . Win {opts -prefix -fmt -label -aval -vval -start -notop}
    # Dump a treeview to XTL.
    array set p {-prefix {} -fmt 1 -label 1 -aval {} -vval {} -start 0 -notop 0}
    array set p $args
    if {!$p(-notop)} {
        set rc [_TreeDump1 $w $p(-start)]
    } else {
        set rc [_TreeDump $w $p(-start)]
    }
    if {$p(-fmt)} { set rc [FmtTree $rc] }
    return $rc
}

proc ::blt::tv::WNew {cmd args} {
    # Use style commands if possible.
    if {[info exists ::Tk::Wins]} {
        return [eval $cmd new $args]
    }
    return [eval $cmd $args]
}


proc ::blt::tv::XTLLoad {args} { #TYPES: win {opts -altcolor -colopts -conf -data -eval -refresh -titles -win} 
    # Load a flat table.
    array set p {
        -altcolor   *
        -colopts    {}
        -conf       {}
        -data       {}
        -eval       {}
        -refresh    0
        -titles     {}
        -win        {}
    }
    variable pc
    array set p $args
    set data $p(-data)
    if {$p(-eval) != {}} {
        set data [eval $p(-eval)]
    }
    if {$data == {}} {
        error "Must provide -data"
    }
    set titles $p(-titles)
    if {$titles == {}} {
       set titles {Name Value}
    }
    set colors $pc(colors)
    set idx 1
    if {[set t $p(-win)] != {}} {
        if {$p(-refresh) && ![winfo exists $p(-win)]} return
        $t delete all
    } else {
        while {[winfo exists [set w .__tvdatatable$idx]]} {
            incr idx
        }
        WNew Toplevel $w
        set f $w.f
        WNew Frame $f
        grid $f -row 10 -column 10 -sticky news
        grid columnconf $w 10 -weight 1
        grid rowconf $w 10 -weight 1
        set t $f.t
        WNew Scrollbar $f.sv -command "$t yview"
        WNew Scrollbar $f.sh -command "$t xview" -orient horizontal
        WNew TreeView $t -width 600 -autocreate 1 -yscrollcommand "$f.sv set" -xscrollcommand "$f.sh set" -bg white -underline 1
        grid $t $f.sv
        grid $f.sh -sticky we
        grid conf $t -sticky news
        grid conf $f.sv -sticky ns
        grid columnconf $f 0 -weight 1
        grid rowconf $f 0 -weight 1
        
    }
    #$t conf -font  {Verdana 14 bold}; $t conf -titlefont [$t cget -font]
    if {$p(-altcolor) != {}} {
        if {[set color $p(-altcolor)] == "*"} {
            set color [lindex $colors [expr {($idx-1)%[llength $colors]}]]
        }
        catch {
            $t style create textbox alt -bg $color
            $t conf -altstyle alt -selectbackground SteelBlue -nofocusselectbackground SteelBlue

        }
    }
    TreeLoad $t $data
    eval $t col conf [$t col names] -bd 1 -relief raised -autowidth 250
    $t col conf 0 -title Tag
    $t col conf Value -justify left -titlejustify left
    if {$p(-colopts) != {}} {
        foreach i [$t col names] { eval [list $t column conf $i] $p(-colopts) }
    }
    if {$p(-conf) != {}} {
        eval $t conf $p(-conf)
    }
    if {$p(-refresh) > 0} {
        set p(-win) $t
        set p(-altcolor) {}
        set p(-conf) {}
        after $p(-refresh) [concat [namespace current]::TableLoad [array get p]]
    }
    return $t
}

proc ::blt::tv::TableLoad {args} { #TYPES: win {opts -altcolor -colopts  -colprefix -conf -data -eval -refresh -subfield -split -titles -ititles -treefield -win} 
    # Load a flat table.
    variable pc
    array set p {
        -altcolor   *
        -colopts    {}
        -colprefix  F
        -conf       {}
        -data       {}
        -eval       {}
        -refresh    0
        -subfield   {}
        -split      False
        -titles     {}
        -ititles    False
        -treefield  {}
        -win        {}
    }
    array set p $args
    set data $p(-data)
    if {$p(-eval) != {}} {
        set data [eval $p(-eval)]
    }
    if {$p(-split)} {
        set data [split $data \n]
    }
    if {$data == {}} {
        error "Must provide -data"
    }
    set titles $p(-titles)
    if {$p(-ititles)} {
        set titles [lindex $data 0]
        set data [lrange $data 1 end]
    }
    set colors $pc(colors)
    set idx 1
    if {[set t $p(-win)] != {}} {
        if {$p(-refresh) && ![winfo exists $p(-win)]} return
        $t delete all
    } else {
        while {[winfo exists [set w .__tvdatatable$idx]]} {
            incr idx
        }
        WNew Toplevel $w
        set f $w.f
        WNew Frame $f
        grid $f -row 10 -column 10 -sticky news
        grid columnconf $w 10 -weight 1
        grid rowconf $w 10 -weight 1
        set t $f.t
        WNew Scrollbar $f.sv -command "$t yview"
        WNew Scrollbar $f.sh -command "$t xview" -orient horizontal
        WNew TreeView $t -width 600 -autocreate 1 -yscrollcommand "$f.sv set" -xscrollcommand "$f.sh set" -bg white -underline 1
        grid $t $f.sv
        grid $f.sh -sticky we
        grid conf $t -sticky news
        grid conf $f.sv -sticky ns
        grid columnconf $f 0 -weight 1
        grid rowconf $f 0 -weight 1
        
    }
    #$t conf -font  {Verdana 14 bold}; $t conf -titlefont [$t cget -font]
    if {$p(-altcolor) != {}} {
        if {[set color $p(-altcolor)] == "*"} {
            set color [lindex $colors [expr {($idx-1)%[llength $colors]}]]
        }
        catch {
            $t style create textbox alt -bg $color
            $t conf -altstyle alt -selectbackground SteelBlue -nofocusselectbackground SteelBlue

        }
    }
    if {$p(-treefield) != {}} {
        $t column conf 0 -relief raised -bd 1 -title $p(-treefield)
    } else {
        $t column conf 0 -hide 1
    }
    set data0 [$t column names]
    foreach i $data {
        while {[llength $data0] <= [llength $i]} {
            set cn [lindex $titles [expr {[llength $data0]-1}]]
            if {$cn == {}} {
                set cn $p(-colprefix)[llength $data0]
            }
            $t column insert end $cn  -justify left -relief raised -bd 1 -pad 10 -editopts {-autonl 1} -command [list blt::tv::SortColumn %W %C]
            set data0 [$t column names]
        }
        set d {}
        set n 0
        array unset q
        foreach j $i {
            set ii [lindex $data0 [incr n]]
            lappend d $ii $j
            set q($ii) $j
        }
        if {$p(-treefield) == {}} {
            set path #auto
        } else {
            set path $q($p(-treefield))
        }
        $t insert end $path -data $d
    }
    if {$p(-subfield) != {}} {
        foreach i [$t find] {
            set id [$t entry set $i $p(-subfield)]
            if {$id == {}} continue
            set did [$t find -name $id]
            if {$did == {}} continue
            #puts "ID($i) id=$id, did=$did"
            if {[string equal $did $i]} continue
            $t move $i into $did
        }
    }
    $t open -trees root
    bind . <Control-Alt-Insert> "console show"
    if {$p(-colopts) != {}} {
        foreach i [$t col names] { eval [list $t column conf $i] $p(-colopts) }
    }
    if {$p(-conf) != {}} {
        eval $t conf $p(-conf)
    }
    if {$p(-refresh) > 0} {
        set p(-win) $t
        set p(-altcolor) {}
        set p(-conf) {}
        after $p(-refresh) [concat [namespace current]::TableLoad [array get p]]
    }
    return $t
}

proc ::blt::tv::EditValid {wconf t newdata ind} {
    # The following uses validate to prevent invalid edit from completing.
    set nam [$t entry set $ind Name]
    if {[catch {eval $wconf [list $nam $newdata]} rv]} {
        return -code 10 $rv
    }
    return $newdata
}

proc ::blt::tv::TableWid {wconf} {
    # Edit widget configure info in a table.
    set w [lindex $wconf 0]
    if {[llength $wconf] == 1} { lappend wconf configure }
    set data [lsort -dictionary [eval $wconf]]
    set t [blt::tv::TableLoad -data $data -titles {Name DBName DBClass Default Value Type}]
    wm title [winfo toplevel $t] "Widget Info: [winfo class $w] [winfo name $w] '[lrange $wconf 1 end]' in [winfo parent $w]"
    $t col move Value DBName
    $t col move Default DBName
    eval $t col conf [$t col names] -bg LightGray
    $t col conf Value -edit 1 -titleforeground LimeGreen -titlejustify left -bg White
    $t col conf Value -validatecmd [list [namespace current]::EditValid $wconf %W %V %#]
    return $t
}

proc ::blt::tv::TreeFill {w str args} {
    # Load treeview with data indented by 4 space multiples (converts tabs to 4).
    # If -flat, load as a table and ignore indents.
    set cols [$w column names]
    set tstr [string trim $str]
    set inttl 0
    set istable [$w cget -flat]
    set sind [expr {$istable?0:1}]
    if {[llength $cols] == 1} {
        set inttl 1
        set s0 [string first \n $tstr]
        if {$s0<0} {
            set str0 $str
            set str {}
        } else {
            set str0 [string range $tstr 0 [incr s0 -1]]
            set s0 [string first \n $tstr]
            set str [string range $tstr [incr s0] end]
        }
        set cols $str0
        set titles [lrange $cols $sind end]
        foreach i $titles {
            $w column insert end $i
        }
        if {!$istable} {
            set col0 [lindex $cols 0]
            $w column conf 0 -title $col0
        }
    } else {
        set titles [lrange $cols $sind end]
        if {[lindex $cols 0] != "#0"} { error "tree col must be first" }
    }
    if {$istable} {
    } else {
        set str [string map {\t {    }} $str]
    }
    set lst [split $str \n]
    if {$istable} {
        foreach i $lst {
            set data {}
            foreach j $i k $titles {
                if {$k == {}} break
                if {$j != {}} {
                    lappend data $k $j
                }
            }
            $w insert end #auto -data $data
        }
    } else {
        set msg {}
        while {[string trim [lindex $lst 0]] == {} && [llength $lst]>1} {
            set lst [lrange $lst 1 end]
        }
        set l0 [lindex $lst 0]
        set l0a [string trimleft $l0]
        set sp0 [expr {[string length $l0]-[string length $l0a]}]
        set at 0
        set n 0
        foreach i $lst {
            incr n
            set lbl [lindex $i 0]
            set ii [lrange $i 1 end]
            set la [string trimleft $i]
            if {$la == {}} continue
            set sp [expr {[string length $i]-[string length $la]}]
            set lev [expr {($sp-$sp0)/4}]
            set mod [expr {($sp-$sp0)%4}]
            if {$mod && $msg == {}} {
                set msg "treeview data indent ($mod) not divisible by 4 in: '$i'"
            }
            set data {}
            foreach j $ii k $titles {
                if {$k == {}} {
                    set k [$w column insert end #auto]
                    lappend titles $k
                }
                if {$j != {}} {
                    lappend data $k $j
                }
            }
            if {$lev<=0 || $n==1} {
                set at 0
            } else {
                set at [$w index tail]
                while {[$w entry depth $at]>$lev} {
                    set at [$w entry parent $at]
                }
            }
            $w insert end [list $lbl] -at $at -data $data
        }
        if {$msg != {}} {
            tclLog $msg
        }
    }
}


if {$argv0 == [info script]} {
    if {[llength $argv]} {
       return [eval ::blt::tv::TableLoad $argv]
    }

  pack [treeview .tt ] -side left -fill both -expand y
  variable tree {
    A 1
    A 2
    {B - -X 1 -Y 2} 2
    {C +} {
        a 1
        b 2
        {c - -X 3}  2
        {d +} {
            x 1
        }
    }
  }

  ::blt::tv::TreeLoad .tt $tree -trim - -nice 1
  tclLog [::blt::tv::TreeDump .tt] 
  pack [treeview .tf ] -side left -fill both -expand y
  ::blt::tv::TreeFill .tf {
    A 1 2 3
    C 1 2 3
    B 1 2 3
        1 1 2 3
        2 1 2 3
            a 1 2 3
            b 1 2 3
  }
  .tf open [.tf find -istree]

  namespace eval ::blt::tv {
  TableLoad -titles  {Name Alpha Bravo Charlie Detroit Foxtrot} -data {
            {Bob 9 21 9}
            {Derick 2 1 5}
            {Bill 3 2 5 2 1}
        }
  if {$::tcl_platform(platform) == "unix"} {
     TableLoad -eval {exec df} -ititles 1 -split 1
     TableLoad -ititles 1 -treefield PID -subfield PPID -split 1 -eval {exec ps -eo comm,uid_hack,rss,sz,time,pid,ppid,tty}
     TableLoad -ititles 1 -data [split [exec ps -Alwj] \n]
     TableLoad -ititles 1 -data [array get ::env] -llength 2

     proc LoadPs {} {
        set data [split [string trim [exec ps auxw]] \n]
        set ttl [lindex $data 0]
        set lst {}
        lappend lst $ttl
        set pos [string last [lindex $ttl end] $ttl]
        foreach i [lrange $data 1 end] {
          set nl [string range $i 0 [expr {$pos-1}]]
          lappend nl [string range $i $pos end]
          lappend lst $nl
        }
        return $lst
     }
     TableLoad -ititles 1 -eval {LoadPs} -refresh 3000
     #eval TableLoad [lrange $argv $n end]
    }
    }

}

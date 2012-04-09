#!/usr/bin/env python
# Password on clipboard

# Boilerplate PyGTK env init:
import pygtk
pygtk.require('2.0')
import gtk

icon_xpm_data = [
"32 32 399 2","   c #000000"," . c #B1B1B1"," X c #D48300"," o c #948C84"," O c #EBB909"," + c #FBF7B4",
" @ c #98801E"," # c #A9A9A9"," $ c #F6D96D"," % c #CA7400"," & c #A7A7A7"," * c #F4DA61"," = c #070700",
" - c #F3D100"," ; c #E7BF1C"," : c #6E4D23"," > c #F3CB00"," , c #C69E16"," < c #584200"," 1 c #D89C00",
" 2 c #E3BF04"," 3 c #E5B210"," 4 c #979797"," 5 c #C4A400"," 6 c #E9B800"," 7 c #959595"," 8 c #FFFA9D",
" 9 c #291F00"," 0 c #E9B000"," q c #D88C00"," w c #A97D00"," e c #7F7D51"," r c #DAA019"," t c #919191",
" y c #040300"," u c #E09E0B"," i c #9F7800"," p c #BD8903"," a c #DACE9D"," s c #FFFAB4"," d c #878787",
" f c #FFFFD5"," g c #FFFDD5"," h c #A4813D"," j c #FFFAA0"," k c #070706"," l c #F8D601"," z c #F7D600",
" x c #818181"," c c #FFFB96"," v c #FFFFC1"," b c #D58600"," n c #7D7D7D"," m c #D58400"," M c #DDAB01",
" N c #C19000"," B c #C18E00"," V c #D2B000"," C c #FEFEB6"," Z c #5C4500"," A c #D0C54A"," S c #8B730D",
" D c #CB8100"," F c #777777"," G c #7B6C1B"," H c #757575"," J c #737373"," K c #847C27"," L c #717171",
" P c #6F6F6F"," I c #EDCD42"," U c #8C7A1B"," Y c #080600"," T c #FEEF42"," R c #6D6D6D"," E c #6B6B6B",
" W c #FFFCBA"," Q c #696969"," ! c #D28000"," ~ c #E3A200"," ^ c #D27E00"," / c #676767"," ( c #997400",
" ) c #656565"," _ c #FFFDDB"," ` c #FCE101"," ' c #C87900"," ] c #313128"," [ c #FFF67B"," { c #FFFCA6",
" } c #FFFAA6"," | c #616161",".  c #AAA642",".. c #F5DD64",".X c #FFFB9C",".o c #5D5D5D",".O c #E7B928",
".+ c #CF9000",".@ c #5B5B5B",".# c #3B2C00",".$ c #4F4538",".% c #F1C000",".& c #535353",".* c #EEDF74",
".= c #CFC870",".- c #66665F",".; c #FFFCA9",".: c #F4CE1A",".> c #8C8781","., c #515151",".< c #BFBEB3",
".1 c #F3CA19",".2 c #4F4F4F",".3 c #F2E22F",".4 c #8C8942",".5 c #776313",".6 c #040402",".7 c #494949",
".8 c #D3B500",".9 c #C28F00",".0 c #EBDB88",".q c #FBF491",".w c #8A7140",".e c #FFFDE1",".r c #F4E769",
".t c #ECE7A0",".y c #F4E994",".u c #3F3F3F",".i c #E9B505",".p c #6A6948",".a c #DCDBCF",".s c #F5CF00",
".d c #B18F45",".f c #353535",".g c #E4A500",".h c #D38100",".j c #333333",".k c #FFFFE4",".l c #11110B",
".z c #9A7500",".x c #F7E36F",".c c #313131",".v c #AB9300",".b c #FFFAAF",".n c #876F40",".m c #F6DF6E",
".M c #2F2F2F",".N c #FCE200",".B c #F5D117",".V c #2D2D2D",".C c #100C00",".Z c #2B2B2B",".A c #FFFDD0",
".S c #F9EA7E",".D c #F0D368",".F c #422D06",".G c #6B6B63",".H c #A1782B",".J c #1F1F1F",".K c #D07900",
".L c #1D1D1D",".P c #A4A287",".I c #FCF284",".U c #907859",".Y c #685A00",".T c #191919",".R c #D79000",
".E c #171717",".W c #DBD9D4",".Q c #FFFB94",".! c #030300",".~ c #131313",".^ c #E6C14A","./ c #C2C2C2",
".( c #FFFCB5",".) c #FFFAB5","._ c #CD7B00",".` c #141100",".' c #BCBCBC",".] c #69685A",".[ c #F2E466",
".{ c #55514D",".} c #705501",".| c #090909","X  c #FFFCA1","X. c #050505","XX c #2F1A00","Xo c #F6D200",
"XO c #030303","X+ c #B4B4B4","X@ c #E5AA00","X# c #010101","X$ c #B2B2B2","X% c #D48200","X& c #B0B0B0",
"X* c #C08E00","X= c #9B7400","X- c #FCE209","X; c #ACACAC","X: c #FDE500","X> c #C2AF65","X, c #DB9D00",
"X< c #514200","X1 c #ECBB00","X2 c #201F12","X3 c #A8A8A8","X4 c #110900","X5 c #FFFB9A","X6 c #A4A4A4",
"X7 c #261904","X8 c #A2A2A2","X9 c #F3CC00","X0 c #3D3000","Xq c #F3C800","Xw c #9E9E9E","Xe c #221300",
"Xr c #A2A063","Xt c #E6E6DE","Xy c #9C9C9C","Xu c #C3C2B5","Xi c #CEA200","Xp c #FADD00","Xa c #0E0700",
"Xs c #C76D00","Xd c #694F00","Xf c #929292","Xg c #866602","Xh c #F2E34E","Xj c #FFFCBE","Xk c #8E8E8E",
"Xl c #8C8C8C","Xz c #FFFFDF","Xx c #564101","Xc c #CBAA00","Xv c #DF9A00","Xb c #5F5017","Xn c #332303",
"Xm c #868686","XM c #FDFCA8","XN c #E5AD13","XB c #FFFBA0","XV c #F4CB11","XC c #D59300","XZ c #828282",
"XA c #F2E45B","XS c #868447","XD c #BA7200","XF c #808080","XG c #F7D300","XH c #7E7E7E","XJ c #010000",
"XK c #FBF267","XL c #DFA603","XP c #C18F00","XI c #5C4600","XU c #F5E96B","XY c #FAF587","XT c #767676",
"XR c #302F2E","XE c #B8994D","XW c #F8EF85","XQ c #DC9400","X! c #CCAF50","X~ c #FFFDCE","X^ c #493801",
"X/ c #FFFA99","X( c #6E6E6E","X) c #6C6C6C","X_ c #E5A902","X` c #FFF364","X' c #6A6A6A","X] c #686868",
"X[ c #BE8D00","X{ c #E8B11C","X} c #D27D00","X| c #6A6960","o  c #666666","o. c #FFFCB0","oX c #646464",
"oo c #715007","oO c #F9E429","o+ c #FFFDD1","o@ c #606060","o# c #C86E00","o$ c #DA8E01","o% c #D98E00",
"o& c #605300","o* c #747463","o= c #D8B602","o- c #050300","o; c #F6EEA7","o: c #604B00","o> c #F3D12D",
"o, c #201800","o< c #585858","o1 c #F8E574","o2 c #E5AC26","o3 c #FFFCB3","o4 c #CAAE33","o5 c #6B6A5A",
"o6 c #E09B00","o7 c #525252","o8 c #505050","o9 c #575643","o0 c #BABAB8","oq c #F6DA68","ow c #E7B600",
"oe c #4C4C4C","or c #F4E027","ot c #7E7727","oy c #FFFDC0","ou c #D68600","oi c #020100","op c #B8B3AC",
"oa c #464646","os c #B79A5F","od c #9B7333","of c #424242","og c #FFF156","oh c #D8D45E","oj c #D98F10",
"ok c #FAEC5B","ol c #404040","oz c #DD9500","ox c #3E3E3E","oc c #C27800","ov c #E8B604","ob c #FFFAA2",
"on c #484620","om c #D4CF50","oM c #383838","oN c #FFFDC3","oB c #F5D000","oV c #241B00","oC c #EBC049",
"oZ c #363636","oA c #FEFEB8","oS c #DAAB00","oD c #B86500","oF c #323232","oG c #303030","oH c #6B5900",
"oJ c #C97100","oK c #FFFDC6","oL c #C09E2F","oP c #323114","oI c #060400","oU c #262626","oY c #E1B000",
"oT c #ECC343","oR c #242424","oE c #D5D5D5","oW c #F1D15F","oQ c #222222","o! c #202020","o~ c #1E1E1E",
"o^ c #5D5548","o/ c #1C1C1C","o( c #BBBBB8","o) c #E5DC74","o_ c #1A1A1A","o` c #C09711","o' c #FFFCD3",
"o] c #181818","o[ c #C9C9C9","o{ c #E8BE21","o} c #E5DF95","o| c #706640","O  c #030200","O. c #F5E848",
"OX c #C39300","Oo c #EEC63E","OO c #F3D65A","O+ c #121212","O@ c #E0CA6F","O# c #101010","O$ c #F3D950",
"O% c #0E0E0E","O& c #BFBFBF","O* c #BDBDBD","O= c #543F00","O- c #FFFAAB","O; c #0A0A0A","O: c #CD7400",
"O> c #FFF14B","O, c #EEDE6C","O< c #080808","O1 c #FFFFCC","O2 c #060606","O3 c #E5B500","O4 c #F6D300",
"O5 c #F6D100","O6 c #D58901","O7 c #866431","O8 c #B3B3B3","O9 c #EBCD09","O0 c #FFEF37","Oq c #CFAD3D",
"Ow c None",
"OwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwX.O+.~O2OwOwOwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwOwOwOwOwoM E 7 7XlXF.2.LOwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwOwOw.Eo X; # 4Xm n nXT |o_OwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwOwoRX6.' 7XH L P R EX]oXo8O%OwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwo]Xk./XyXTX(X'X] Q Q ).@o<oQOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOw no[Xw H ) /.o.,.@ E Qo7oe.jOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwoRO&O&XZ.&.@o8o]Ow.cXF F.7.uoZOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwo@oEX3o8oFoa.|OwOw.ZXy dox.coFOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwO#Xlo[ t.cof.JOw k ]o*o0 7.foU.VOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOw.T #O* xo~o<.-.Po}XWo).aX8oG.J.ponOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwo/X+O8 Jo!.].rXhXUXW.tXt &.M.J eohoPOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwo9o(O8X(o!o5 + g.AoK a.WX3oF.Jo|XK. OwOwOwOwOwOw",
"OwOwOwOwOwOwX2Xr.=XuX$X)o!.Go+X~oKXjos oXfolXR :XAomOwOwOwOwOwOw",
"OwOwOwOwOwOwXSO. A.< .X'o!X|oNoy Wo3.0.d.w.n.HOqoko4OwOwOwOwOwOw",
"OwOwOwOwOwOw.4.3X>opX&o<o!o^o;.(o..;XB.q.*O,.[O$ r pOwOwOwOwOwOw",
"OwOwOwOwOwOwooo{oL.U.>.{.$O7.y {X .X.Q.I..oTojoJXDX[OwOwOwOwOwOw",
"OwOwOwOwOwOw GX{.^X! hodXEO@.XX5 c.SoCo2 uo$.hO: 'X*OwOwOwOwOwOw",
"OwOwOwOwOwOwot.Bov.O *.xo1.mOOOoXNX@owoS 0 ~ qX} ^ BOwOwOwOwOwOw",
"OwOwOwOwOwOwot.B -O9 I.DoWo>X9.soB 5X<X0XgXLozX%X%.9OwOwOwOwOwOw",
"OwOwOwOwOwOwot.BXoorXY CX/O0X:Xp.v.`  o-Xno`Xv b m.9OwOwOwOwOwOw",
"OwOwOwOwOwOwot.BXGoOXM v 8O0X:Xpo&  XJXa.F ,o6ou X.9OwOwOwOwOwOw",
"OwOwOwOwOwOwot.BXGX-oAO1obO0X:Xp.YoioIX7 @ 3Xv.h !XPOwOwOwOwOwOw",
"OwOwOwOwOwOwot.BXG ` j f }O0X:Xp.8oHX4Xb ;X_XQ.K._X*OwOwOwOwOwOw",
"OwOwOwOwOwOwot.BXG ` [XzO-O0X:XpO4XcXe.5 O.g ^Xsoc NOwOwOwOwOwOw",
"OwOwOwOwOwOw K.BXG `X`.k.bO0X:XpO4 VXX S.io%o#oD.+ wOwOwOwOwOwOw",
"OwOwOwOwOwOw UXVXG `og.e sO0X:XpO4 >o= 2O6 % D 1 (o,OwOwOwOwOwOw",
"OwOwOwOwOwOwX^ MO5 `O> _.)O0X:XpO4 > 6XC.RX,X=O=OwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwXIO3 l To'.)O0.N zXqX1OX i <.COwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwo:Xi.1 $oq.:.%oY.z Z 9OwOwOwOwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOw =.#Xd.}XxoVO OwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOw",
"OwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOwOw"]

# A class for HelloWorld window
class PasswordClipboard:
    def quit_handler(self, widget, *args):
        self.clear_clipboard()
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Password to Clipboard")
        self.window.set_default_size(500,50)
        self.window.set_border_width(10)
        self.window.set_resizable(False)
        self.window.set_keep_above(True)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        #self.window.set_position(gtk.WIN_POS_CENTER)
        #self.window.move(100, 100)

        
        accel_group = gtk.AccelGroup()
        accel_group.connect_group(ord('q'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_LOCKED, self.quit_handler)
        self.window.add_accel_group(accel_group)

        self.window.connect("delete_event", self.quit_handler)
        self.window.connect("destroy", self.quit_handler)
        
        # Container for all buttons and input field
        self.vbox = gtk.VBox(False, 10)
        self.window.add(self.vbox)

        self.hbox1 = gtk.HBox(False, 2)
        self.input_label = gtk.Label("Password:")
        self.hbox1.pack_start(self.input_label, True, True, 0)
        
        self.entry = gtk.Entry(15)
        self.entry.set_visibility(False)
        self.entry.connect("activate", self.set_clipboard_handler)
        self.entry.connect("activate", self.warning_mode_handler)
        self.hbox1.pack_start(self.entry, True, True, 0)

        self.status_label = gtk.Label("")
        
        self.hbox2 = gtk.HBox(False, 0)
        self.button_quit = gtk.Button("Clear clipboard and _exit")
        self.button_quit.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.button_quit.set_use_underline(True)
        self.hbox2.pack_start(self.button_quit, True, True, 0)

        self.vbox.pack_start(self.hbox1, True, True, 0)
        self.vbox.pack_start(self.status_label, True, True, 0)
        self.vbox.pack_end(self.hbox2, True, True, 0)
        
        self.input_label.show()
        self.entry.show()
        self.hbox1.show()
        self.status_label.show()
        self.button_quit.show()
        self.hbox2.show()
        self.vbox.show()
        self.window.show()
        
        # Set up window icon and move it to top left corner
        self.window.set_icon(gtk.gdk.pixbuf_new_from_xpm_data(icon_xpm_data))
        width, height = self.window.get_size()
        self.window.move(gtk.gdk.screen_width() - width - 10, 30)

        self.normal_color = self.window.style.bg[gtk.STATE_NORMAL]
        self.warn_color = gtk.gdk.color_parse('#F76767')

    def warning_mode_handler(self, widget):
        if len(widget.get_text()) > 0:
            self.window.modify_bg(gtk.STATE_NORMAL, self.warn_color)
            self.status_label.set_text("PASSWORD SET")
        else:
            self.window.modify_bg(gtk.STATE_NORMAL, self.normal_color)
            self.status_label.set_text('')

    def set_clipboard_handler(self, widget):
        # get the clipboard:
        clipboard = gtk.clipboard_get()
        # set the clipboard text data:
        clipboard.set_text(widget.get_text() + '\n')
        # make our data available to other applications:
        clipboard.store()
    
    def clear_clipboard(self):
        gtk.clipboard_get().clear()


        
def main():
    gtk.main()

if __name__ == "__main__":
    hello = PasswordClipboard()
    main()

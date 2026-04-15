//-------------------------------------------------------------------
// title: DIN clip
// authors: OK1HRA, Felipe Bombardelli
// license: Creative Commons BY-SA
// URL: http://remoteqth.com/3d-din-rail-mount-clip.php
// revision: 0.2
// format: OpenSCAD
//-------------------------------------------------------------------
// HowTo:
// After open change inputs parameters and press F5
// .STL export press F6 and menu /Design/Export as STL...


// ==================================================================
//  Input parameter
// ==================================================================

// $fn=50;

// ==================================================================
//  Examples
// ==================================================================

// Exemplo
// din_clip_2h(100, first=-20);
// translate([35,0,0]) din_clip_2h(75,-20);
// translate([70,0,0]) din_clip_2v(30,30,first=10);

// LCD de 10.5 polegadas
// din_clip_2h(115, -43.5, width=8, identation=8);

// Ponte H Vermelha
// din_clip_2h(37.5); 

// Ponte H
// din_clip_2h(46);

// DFROBOT Tracker Sensor V4idente
// din_clip_1(20.5, identation=5);

// Sensor de Humidade
// din_clip_1(32);

// RFID-RC522
// din_clip_2v(30, 38);  

// DFROBOT Led - arrumar
// din_clip_2v(10, -10, first=10.5+22.5, screw=1.49);  

// DFROBOT Buzzer V2
// din_clip_2v(15, 15, screw=1.49);  

// DFROBOT Gas Sensor V2
// din_clip_2v(20, 30, screw=1.49);

// DFROBOT OLED-2864 Display V1.1
// din_clip_2v(35, 20, screw=1.49);

// ESP32 com placa
// din_clip_2v(35, 73, screw=1.49, width=8);


// ==================================================================
//  Clip Base
// ==================================================================

module din_clip(distance, first=10.5, width=6, screw=1.49, expand=1, hole1=true, hole2=true, hole3=true) {
    long = 45;  // tamanho do clip, dificilmente mudará
    second = distance + first;
    
    // First hole is not be between -2 to 10.5
    if ( first > -2.0 && first < 10.5 ) {
        echo("WARNING: the first pin must be greater than 10.5 or less than -2");
    }
    
	difference() {
		union() {
			hull() {
				translate([15+expand,long-2,0]) {cylinder(h=width, r=2, center=false);}
                translate([12+expand,37.5,0]) {cube([5,1,width], center=false);}
                translate([12+expand,long-1,0]) {cube([1,1,width], center=false);}
            }
			hull() {
				translate([16+expand,35.7,0]) {cylinder(h=width, r=1, center=false);}
                translate([14.2+expand,37.5,0]) {cube([2.8,1,width], center=false);}
            }
			hull() {
				translate([20+expand,0.5,0]) {cylinder(h=width, r=0.5, center=false);}
				translate([14.5+expand,4.25,0]) {cylinder(h=width, r=0.3, center=false);}
				translate([14.2+expand,0,0]) {cube([1,1,width], center=false);}
			}


            if ( first > 0 ) {
                translate([0,1.5,0]) cube([3.5,2,width], center=false);
            } else {
                translate([0,-1,0]) cube([3.5,4,width], center=false);
            }


            cube([15+expand,2,width], center=false);
			hull() {
				translate([12+expand,4,0]) {cylinder(h=width, r=1, center=false);}
                translate([0,3,0]) {cube([1,1,width], center=false);}
                translate([0,long-1,0]) {cube([13+expand,1,width], center=false);}
            }
            
            // Second Support
			hull() {
                translate([0,40,0]) {cube([14,1,width], center=false);}
                translate([2,second+3,0]) {cylinder(h=width, r=2, center=false);}
                translate([6,second+3,0]) {cylinder(h=width, r=2, center=false);}
            }
            
            // Case First Pin is negative
            if ( first < 0 ) {
                translate([0,first,0]) cube([7,(-first)-1,width], center=false);
                hull() {
                    translate([0,first,0]) {cube([7,1,width], center=false);}
                    translate([2,first-3,0]) {cylinder(h=width, r=2, center=false);}
                    translate([6,first-3,0]) {cylinder(h=width, r=1, center=false);}
                }
            }

        }
        translate([3.5,2.5,-1]) {cylinder(h=width+2, r=0.5, center=false);}
        translate([3.5,-0.5,-1]) {cylinder(h=width+2, r=0.5, center=false);}
        
        // aretation
        translate([9+expand,-1,width/2]) rotate([-90,0,0]) {
            cylinder(h=9, r=screw, center=false);
        }
        // translate([6.15+expand,5,-1]) {cube([5.7,4,width+2], center=false);}
       
        // 3. Vazio no meio da peça para econimizar plastico
        if ( hole1 ) {
            translate([3,12,-1]) {cube([7,13.5,width+2], center=false);}
        }
        
        if ( hole2 ) {
            translate([3,28.5,-1]) {cube([7,13.5,width+2], center=false);}
        }
        
        if ( hole3 && (distance+first) > 50 ) {
            hull() {
                translate([3,45,-1]) {cube([7,1,width+2], center=false);}
                translate([4.8,second-3,-1]) {cylinder(h=width+2, r=1.8, center=false);}
            }
        }
        
    }
    
}

// ==================================================================
//  Clips
// ==================================================================

module din_clip_1(first=10.5, width=6, screw=1.49, expand=1, hole1=true, hole2=true, hole3=true, identation=3){

    difference() {
        // Desenha toda a peça
        union() {
            din_clip(2, first=first, width=width, screw=screw, hole1=hole1, hole2=hole2, hole3=hole3);
            translate([-identation,first-3.5,0]) cube([identation+1,7,width], center=false);
        }
        
        // Coloca o buraco para o parafuso 1
        translate([-identation-1, first, width/2]) rotate([0,90,0]) {
            cylinder(h=6+expand+identation, r=screw, center=false);
        }
    }
}

module din_clip_2h(distance, first=9.5, width=6, screw=1.49, expand=1, hole1=true, hole2=true, hole3=true, identation=3){
    second = distance + first;
    difference() {

        // Desenha toda a peça
        union() {
            din_clip(distance, first=first, width=width, screw=screw, hole1=hole1, hole2=hole2, hole3=hole3);
            translate([-identation,first-3.5,0]) cube([identation+1,7,width], center=false);
            translate([-identation,-3.5+second,0]) cube([identation+1,7,width], center=false);
        }
        
        // Coloca o buraco para o parafuso 1
        translate([-identation-1, first, width/2]) rotate([0,90,0]) {
            cylinder(h=6+expand+identation, r=screw, center=false);
        }
        
        // Coloca o buraco para o parafuso 2
        translate([-identation-1, second, width/2]) rotate([0,90,0]) {
            cylinder(h=6+expand+identation, r=screw, center=false);
        }
    }

    // 3. Segundo suporte para o parafuso
}


module din_clip_2v(distance, distance_support, first=10.5, width=6, screw=1.49, expand=1, identation=3) {
    // 1. Desenha a base do clip
    din_clip_2h(distance_support, first=first, width=width, screw=screw, hole1=false, hole2=false);

    // 2. Segundo suporte para o parafuso na vertical
    first_minus_35 = first - 3.5;
    difference() {
        union() {
            translate([0,first_minus_35,width]) cube([7,7,distance]);
            translate([-identation,first_minus_35,distance]) cube([identation,7,width]);
        }
        translate([-1-identation,first,distance+width/2]) rotate([0,90,0])
            cylinder(h=6+expand+identation, r=screw*1.05, center=false);
    }

    // 2.1. Mao francesa embaixo para impressao
    hull() {
        translate([0,first_minus_35,distance]) cube([0.1,7,0.1]);
        translate([-identation,first_minus_35,distance]) cube([0.1,7,0.1]);
        translate([0,first_minus_35,width+distance-width-4]) cube([0.1,7,0.1]);
    }
    
    // 2.2. Mao francesa lateral
    hull() {
        translate([0,first_minus_35+7,distance+width-1]) cube([7,1,1]);
        translate([0,first_minus_35+7+1.15,distance+width-1]) cube([7,1,1]);
        translate([0,first_minus_35+7,width]) cube([7,1,1]);
        translate([0,first+distance_support,width]) cube([7,0.1,0.1]);
    }
    
    // 2.3. Mao francesa entre eles
    hull() {
        translate([0,first_minus_35+7,distance-4]) cube([0.1,0.1,width+4]);
        translate([-identation,first_minus_35+7,distance]) cube([0.1,0.1,width]);
        translate([0,first_minus_35+7+2,distance-4]) cube([0.1,0.1,width+4]);
    }
}
// ======================================================================
//  Header
// ======================================================================

include <vri_din_clip.scad>
include <BOSL2/std.scad>

$fn = 40;

// ======================================================================
//  Debug
// ======================================================================

* % translate([0,5.5,2.2]) scale([1,1,1]) import("thingverse_redmi8_case.stl");
* % translate([0,-5,85]) rotate([90,0,0]) import("thingverse_redmi8_case_cobekone.stl");

// ======================================================================
//  Modulos
// ======================================================================

module parte_cima() {
    difference() {
        rect_tube(size=[84,17.5], wall=2, h=90, rounding=3);
        translate([-35,-15,10]) cube([70,10,82]);
        translate([-47,-6,25]) cube([10,12,55]);
        translate([17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(2.5,7,1.5);
        translate([17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(5,1.5,1.5);
        
        translate([-17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(2.5,7,1.5);
        translate([-17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(5,1.5,1.5);
    }
}

module parte_baixo() {
    difference() {
        union() {
            rect_tube(size=[84,17.5], wall=2, h=72+2.5, rounding=3);
            translate([-40,-8.75,0]) cube([80,17.5,1]);
        }
        
        // frente
        translate([-35,-15,12]) cube([70,10,82]);
        
        // USB
        translate([-10,-6,-5]) cube([20,10,10]);
        
        translate([17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(2.5,7,1.5);
        translate([17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(5,1.5,1.5);
        
        translate([-17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(2.5,7,1.5);
        translate([-17.5,5.5,57.25]) rotate([-90,180,0]) cylinder(5,1.5,1.5);
    }
}

// ======================================================================
//  Main
// ======================================================================

translate([100,0,0]) parte_baixo();
parte_cima();
translate([21.5,10,52]) rotate([0,0,90]) din_clip_2h(34.5,first=10.5-6,width=10,identation=0);



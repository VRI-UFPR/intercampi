// ======================================================================
//  Header
// ======================================================================

// include <BOSL2/std.scad>
// include <BOSL2/walls.scad>
use <vri_din_clip.scad>

// Parametros Configuraveis
altura=40;
espessura=1.5;
// altura_suporte=50;
largura=114.5;

parafuso_comprimento = 10;
parafuso_raio = 1.5;

// ======================================================================
//  Modulos
// ======================================================================

module suporte_para_parafuso() {
    difference() {
        union() {
            cube([5,5,3]);
            hull() {
                translate([0,0, 0]) cube([5,0.25,0.1]);
                translate([0,5,-10]) cube([5,0.25,0.1]);
            
                translate([0,0, 0]) cube([0.25,5,0.1]);
                translate([5,0,-10]) cube([0.25,5,0.1]);
                
                translate([5,5, 0]) cube([0.25,0.25,0.1]);
            }
        }
        translate([2.5,2.5,-5]) cylinder(10,1.5,1.5);
    }

}

module caixa() {
    // Base
    difference() {
        cube([largura,29+8.5,espessura]);
        
        // Espaço para acessar o pino de liga/desliga
        // translate([55,23.5,0]) cube([12.5,7.5,espessura]);
        translate([51,23,-1]) cube([14.5,7,espessura+2]);
        
        # translate([85,13,1]) rotate([0,180,0]) linear_extrude(height = 2) {         text("Intercampi 1", font="sans-serif:style=Bold", size=6);
        }  
    }

    // Tampa ao lado da Pilha
    cube([largura,espessura,altura]);

    // Tampa traseira
    translate([largura-espessura,0,0]) cube([espessura,37.5,altura]);

    // Tampa frontal
    cube([espessura,37.5,altura]);

    // Lateral interna do GPS
    translate([80,28,0]) cube([34,espessura,26.5]);
    translate([0,28,0]) cube([34,espessura,26.5]);

    // Perpendicular para segurar o GPS
    translate([80,32,0]) cube([2*espessura,6,26.5]);
    translate([31,32,0]) cube([2*espessura,6,26.5]);
    
    // Lateral para segurar a placa
    translate([105,21,0]) cube([8,espessura,26.5]);
    
    translate([0,21,0]) cube([10,espessura,26.5]);

    // Tampa Lateral
    translate([0,37.5,0]) cube([largura,espessura,altura]);
    
 
    translate([6.5, 32.5,altura-5]) rotate([0,0,90]) suporte_para_parafuso();
    translate([largura-6.5, 6.5,altura-5]) rotate([0,0,-90]) suporte_para_parafuso();
    
    translate([6.5,6.5,altura-5]) rotate([0,0,180]) suporte_para_parafuso();
    
    
    // translate([35.5,0,0]) cube([espessura,30,altura]);
    // translate([32,19,0]) cube([4,3,altura_suporte]);

    // Lado interruptor
    // cube([espessura,30,altura]);
    // translate([espessura,19,0]) cube([4,3,altura_suporte]);

    // Tampa Frontal
    // translate([0,30,0]) cube([37,espessura,altura]);
}

// Tampa com parafuso sem nenhum texto
module tampa_modelo() {
    difference() {
        union() {
            cube([largura,39,espessura]);
            translate([espessura,espessura,-espessura]) cube([largura-2*espessura,39-2*espessura,espessura]);
        }
        
        // parafuso 1
        translate([largura-2*espessura-1,4,-5])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // parafuso 2
        translate([4,35,-5])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // espaço para USB
        // translate([50,23.5,0]) cube([12,4.5,espessura]);
    }

    // translate([10,25.5,-5]) cube([2.5,2.5,5]);
    // translate([3.5,22.5,-5]) cube([2.5,2.5,5]);
    translate([100,29.6,-9]) cube([2.5,7.8,9]);
}

// Tampa com textos
module tampa() {
    // texto1 = "INTERCAMPI 2";
    // texto2 = "(41) 98827 1051";
    
    translate([0,0,37]) tampa_modelo();
    
    /*
    difference() {
        translate([0,0,37]) tampa_modelo();
        translate([10,12,36]) linear_extrude(height = 8) {
                text(texto1, font="sans-serif:style=Bold", size=9);
            }
            
        translate([20,2,36]) linear_extrude(height = 8) {
            text(texto2, font="sans-serif:style=Bold", size=6);
        }    
    };
    */
}

// ======================================================================
//  Main
// ======================================================================

caixa();
* % tampa();

translate([-1,0,3]) cube([1,14,altura-3]);
translate([-1,14,0]) rotate([90,0,-90]) din_clip(30);

translate([-1+largura+1,0,3]) cube([1,14,altura-3]);
translate([-1+largura+8,14,0]) rotate([90,0,-90]) din_clip(30);

// Mostra o modelo 3D da placa
% translate([51,-83, 47]) rotate([0,180,0]) import("thingverse_ttgo_sim7000.stl");

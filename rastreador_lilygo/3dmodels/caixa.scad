

// Parametros Configuraveis
altura=42;
espessura=1.5;
altura_suporte=50;
largura=115;

parafuso_comprimento = 10;
parafuso_raio = 1.5;

// cube([25,25,7]);

module caixa() {
    // Base
    difference() {
        cube([largura,30,espessura]);
        
        // Espaço para acessar o pino de liga/desliga
        // translate([55,23.5,0]) cube([12.5,7.5,espessura]);
    }

    // Tampa ao lado da Pilha
    cube([largura,espessura,altura]);

    // Tampa traseira
    translate([largura-espessura,0,0]) cube([espessura,30,altura]);

    // Tampa frontal
    // % cube([espessura,30,altura-8]);

    // Lateral interna do GPS
    translate([80,23,0]) cube([34,espessura,altura-espessura]);
    
    //NAOPRECISA translate([0,25,0]) cube([10,espessura,altura-espessura]);

    // Perpendicular para segurar o GPS
    // translate([80,32,0]) cube([2*espessura,6,altura-3*espessura]);
    // translate([31,26,0]) cube([2*espessura,8,altura-espessura]);
    
    // Lateral para segurar a placa
    translate([105,16,0]) cube([8,espessura,altura-espessura]);
    
    translate([0,16,0]) cube([10,espessura,altura-espessura-8]);

    // Tampa Lateral
    translate([0,30,0]) cube([largura,espessura,altura]);
    
 
    // Cilindro para o parafuso
    difference() {
        translate([12,3.5,0]) cylinder(altura-espessura,3,3);
        translate([12,3.5,altura-parafuso_comprimento])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
    }
    difference() {
        translate([largura-3,3,0]) cylinder(altura-espessura,3,3);
        translate([largura-3,3,altura-parafuso_comprimento])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
    }
   
    difference() {
        translate([-21,0,0]) cube([21,30+espessura,34.5]);
        translate([-19+6.25,4+5.25,31.5]) cube([13.5,14.5,4]);
        
        // 
        translate([-21+espessura,espessura,espessura]) cube([21-espessura+1,14.5,23]);
        translate([-21+espessura,espessura+7.25,23]) rotate([0,90,0]) cylinder(21-espessura+1,7.25,7.25);
        
        // 
        translate([-21+espessura,espessura+16,espessura]) cube([21-espessura+1,12.5,23]);
        translate([-21+espessura,espessura+16+6.25,23]) rotate([0,90,0]) cylinder(21-espessura+1,6.25,6.25);
        
    }
    

 
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

    translate([-21,0,-7.5]) difference() {
        cube([21,31.5,9]);
        translate([2,2,-2]) cube([20,27,12]);
    }

    difference() {
        union() {
            translate([espessura,espessura,-espessura]) cube([largura-2*espessura,31.5-2*espessura,espessura]);
            cube([largura,31.5,espessura]);
        }
        
        // parafuso 1
        translate([largura-2*espessura,3,-espessura-1])
            cylinder(parafuso_comprimento+1,parafuso_raio,parafuso_raio);
        
        // parafuso 2
        translate([12,3.5,-espessura-1])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // espaço para USB
        # translate([50.5,15,-espessura-1]) cube([12,8,espessura+5]);
    }
    
    translate([24,espessura,-9]) cube([2,28.5,8]);
}

module gps() {
    // Antena do GPS
    translate([0,0,0]) cube([27,27,5]);
    translate([5.25,5.25,-3]) cube([15,15,3]);
}

// Tampa com textos
module tampa() {
    texto1 = "INTER";
    texto2 = "CAMPI1";
    texto3 = "VRI - UFPR";
    
    difference() {
        translate([0,0,altura]) tampa_modelo();
        translate([12,12,41]) linear_extrude(height = 4) {
            text(texto1, font="sans-serif:style=Bold", size=8);
        }
        
        translate([64,12,41]) linear_extrude(height = 8) {
            text(texto2, font="sans-serif:style=Bold", size=8);
        }
            
        translate([30,2,41]) linear_extrude(height = 8) {
            text(texto3, font="sans-serif:style=Bold", size=6);
        }    
    };
}

// % translate([-19,4,34.5]) cube([25,25,5]);
// % translate([-19+5.25,4+5.25,31.5]) cube([14.5,14.5,3]);

// caixa();
% translate([-19,2,34.5]) gps();
tampa();

// Mostra o modelo 3D da placa
// % translate([65,-88,-11]) rotate([0,0,0]) import("TTGO_SIM7000GV1.stl");


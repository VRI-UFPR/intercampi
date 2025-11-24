

// Parametros Configuraveis
altura=38;
espessura=1.5;
altura_suporte=50;
largura=114;

parafuso_comprimento = 10;
parafuso_raio = 1.5;



module caixa() {
    // Base
    difference() {
        cube([largura,29+8.5,espessura]);
        
        // Espaço para acessar o pino de liga/desliga
        // translate([55,23.5,0]) cube([12.5,7.5,espessura]);
    }

    // Tampa ao lado da Pilha
    cube([largura,espessura,altura]);

    // Tampa traseira
    translate([largura-espessura,0,0]) cube([espessura,37.5,altura]);

    // Tampa frontal
    cube([espessura,37.5,altura]);

    // Lateral interna do GPS
    translate([80,28,0]) cube([34,espessura,altura-3*espessura]);

    // Perpendicular para segurar o GPS
    translate([80,32,0]) cube([2*espessura,6,altura-3*espessura]);
    
    // Lateral para segurar a placa
    translate([105,21,0]) cube([8,espessura,altura-3*espessura]);
    
    translate([0,21,0]) cube([10,espessura,altura-6*espessura]);

    // Tampa Lateral
    translate([0,37.5,0]) cube([largura,espessura,altura]);
    
 
    // Cilindro para o parafuso
    difference() {
        translate([3,36,0]) cylinder(altura-1.5*espessura,3,3);
        translate([3,36,altura-parafuso_comprimento])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
    }
    difference() {
        translate([largura-3,3,0]) cylinder(altura-1.5*espessura,3,3);
        translate([largura-3,3,altura-parafuso_comprimento])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
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
    difference() {
        cube([largura,39,espessura]);
        
        // parafuso 1
        translate([largura-2*espessura,3,0])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // parafuso 2
        translate([3,36,0])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // espaço para USB
        translate([50,23.5,0]) cube([12,4.5,espessura]);
    }
    
    difference() {
        translate([espessura,espessura,-espessura]) cube([largura-2*espessura,39-2*espessura,espessura]);
        
        // parafuso 1
        translate([largura-2*espessura,3,-espessura])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // parafuso 2
        translate([3,36,-espessura])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        
        // espaço para USB
        translate([50,23.5,-espessura]) cube([12,4.5,espessura]);
    }
    
    // translate([10,25.5,-5]) cube([2.5,2.5,5]);
    // translate([3.5,22.5,-5]) cube([2.5,2.5,5]);
    translate([100,29.6,-9]) cube([2.5,7.8,9]);
}

// Tampa com textos
module tampa() {
    texto1 = "INTERCAMPI 2";
    texto2 = "(41) 98827 1051";
    
    difference() {
        translate([0,0,37]) tampa_modelo();
        translate([10,12,36]) linear_extrude(height = 8) {
                text(texto1, font="sans-serif:style=Bold", size=9);
            }
            
        translate([20,2,36]) linear_extrude(height = 8) {
            text(texto2, font="sans-serif:style=Bold", size=6);
        }    
    };
}



caixa();
// tampa();

// Mostra o modelo 3D da placa
translate([65,-83,-11]) rotate([0,0,0]) import("TTGO_SIM7000GV1.stl");


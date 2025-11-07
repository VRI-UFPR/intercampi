

// Parametros Configuraveis
altura=37;
espessura=1.5;
altura_suporte=50;


parafuso_comprimento = 10;
parafuso_raio = 1.5;



module caixa() {
    // Base
    difference() {
        cube([120,29+8.5,espessura]);
        translate([57.5,23.5,0]) cube([20,7.5,espessura]);
    }

    // Tampa ao lado da Pilha
    cube([120,espessura,altura]);

    // Tampa traseira
    translate([120-espessura,0,0]) cube([espessura,37.5,altura]);

    // Tampa frontal
    cube([espessura,37.5,altura]);

    // Lateral interna do GPS
    translate([80,28,0]) cube([40,espessura,altura]);
    
    // Lateral para segurar a placa
    translate([105,21,0]) cube([15,espessura,altura]);
    
    translate([0,21,0]) cube([15,espessura,altura]);

    // Tampa Lateral
    translate([0,37.5,0]) cube([120,espessura,altura]);
    
 
    // Cilindro para o parafuso
    difference() {
        translate([3,36,0]) cylinder(altura,3,3);
        translate([3,36,altura-parafuso_comprimento])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
    }
    difference() {
        translate([117,3,0]) cylinder(altura,3,3);
        translate([117,3,altura-parafuso_comprimento])
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

module tampa() {
    difference() {
        cube([120,39,espessura]);
        translate([117,3,0])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
        translate([3,36,0])
            cylinder(parafuso_comprimento,parafuso_raio,parafuso_raio);
    }
    
    translate([10,25.5,-5]) cube([2.5,2.5,5]);
    translate([3.5,22.5,-5]) cube([2.5,2.5,5]);
    translate([90,29.6,-8]) cube([2.5,7.8,8]);
}


// caixa();

translate([0,0,37]) tampa();

// Mostra o modelo 3D da placa
// translate([65,-83,-11]) rotate([0,0,0]) import("TTGO_SIM7000GV1.stl");


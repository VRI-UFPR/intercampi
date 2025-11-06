

// Parametros Configuraveis
altura=120;
espessura=1.5;
altura_suporte=50;


difference() {
    cube([37,30,3]);
    translate([10,10,0]) cube([10,10,3]);
}






/*
module caixa() {
    // Base
    cube([37,30,1.5]);

    // Tampa Traseira
    cube([37,1.5,altura]);

    // Lado USB
    translate([35.5,0,0]) cube([espessura,30,altura]);
    translate([32,19,0]) cube([4,3,altura_suporte]);

    // Lado interruptor
    cube([espessura,30,altura]);
    translate([espessura,19,0]) cube([4,3,altura_suporte]);

    // Tampa Frontal
    translate([0,30,0]) cube([37,espessura,altura]);
}


difference() {
    caixa();
    // abertura do USB
    translate([35,23.5,50]) cube([3,4.5,25]);
    // abertura do interruptor
    translate([0,23.5,50]) cube([3,4.5,25]);
}



// Mostra o modelo 3D da placa
translate([-10,-83,51]) rotate([0,90,0]) import("TTGO_SIM7000GV1.stl");

*/

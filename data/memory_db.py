#datos demo en memoria

usuarios = {
	"1": {
		"id": 1,
		"nombre": "Usuario Demo A",
		"email": "demo.a@example.com",
		"rut": "11.111.111-1",
		"rol": "Empleado",
		"metodo": "Código QR",
		"activo": True,
		"placeholder": True
	},
	"2": {
		"id": 2,
		"nombre": "Usuario Demo B",
		"email": "demo.b@example.com",
		"rut": "22.222.222-2",
		"rol": "Proveedor",
		"metodo": "Tarjeta RFID",
		"activo": True,
		"placeholder": True
	},
	"3": {
		"id": 3,
		"nombre": "Usuario Demo C",
		"email": "demo.c@example.com",
		"rut": "33.333.333-3",
		"rol": "Visitante",
		"metodo": "Huella Digital",
		"activo": False,
		"placeholder": True
	},
	"4": {
		"id": 4,
		"nombre": "Usuario Demo D",
		"email": "demo.d@example.com",
		"rut": "44.444.444-4",
		"rol": "Empleado",
		"metodo": "Código QR",
		"activo": True,
		"placeholder": True
	}
}

#historial de accesos
logs = [
	{
		"fecha": "14/06/2026 09:15:00",
		"usuario_id": 1,
		"nombre": "Usuario Demo A",
		"metodo": "Código QR",
		"ubicacion": "Vestibulo",
		"estado": "activo",
		"rol": "Empleado",
		"placeholder": True
	},
	{
		"fecha": "14/06/2026 09:20:00",
		"usuario_id": 2,
		"nombre": "Usuario Demo B",
		"metodo": "Tarjeta RFID",
		"ubicacion": "Entrada Lateral",
		"estado": "activo",
		"rol": "Proveedor",
		"placeholder": True
	},
	{
		"fecha": "14/06/2026 09:30:00",
		"usuario_id": 3,
		"nombre": "Usuario Demo C",
		"metodo": "Huella Digital",
		"ubicacion": "Entrada Principal",
		"estado": "inactivo",
		"rol": "Visitante",
		"placeholder": True
	},
	{
		"fecha": "14/06/2026 09:45:00",
		"usuario_id": 4,
		"nombre": "Usuario Demo D",
		"metodo": "Código QR",
		"ubicacion": "Bodega",
		"estado": "activo",
		"rol": "Empleado",
		"placeholder": True
	}
]

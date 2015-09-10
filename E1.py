def galletas (count):
	if count >= 0 and count <= 10:
		return count
	elif count > 10:
		return 'muchas'

def extremos (cad):
	if len(cad) < 4:
		return ''
	else:
		return (cad[0] + cad[1] + cad[len(cad)-2] + cad[len(cad)-1])

def cambiarcar (cad):
	car = cad[0]
	sep = cad[1:]
	ul = sep.replace(car,'*')
	return car + ul
		
E1 = galletas(20)
print (E1)
E2 = extremos('Paulina')
print (E2)
E3 = cambiarcar('avanzar')
print (E3)

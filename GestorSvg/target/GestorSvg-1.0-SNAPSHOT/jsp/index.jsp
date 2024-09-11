<!DOCTYPE html>
<html lang="es">
<head>
<title>Gestor SVG</title>
<link href="/GestorSvg/css/styleSheet.css" rel="stylesheet">
<meta charset="utf-8">
</head>

<body>
	<header>
		<h1>Gestor de imágenes SVG en  base de datos eXist</h1>
		<h2>Sistemas Web 2024</h2>
	</header>

	<%	if (request.getAttribute("informacion") != null) {	%>
	<section>
		<font>Información:</font>
		<%=request.getAttribute("informacion")%>
	</section>
	<% 	} %>
	
	<section>
	 <table><tr>
        <td style="width:150px; background-color:#d7dbdd"><h4>Mostrar las imágenes SVG de una colección</h4></td>
		<td style="width:600px">
			<form id="LeerRecursos" method="GET" action="/GestorSvg/apiLR">
				<table><tr>
					<td>Introducir nombre de la colección:</td>
					<td><input required name="collection"></td>
				</tr></table>			
			<hr>
			<button type="submit" form="LeerRecursos">Ver imagenes</button>
			</form>
		</td>
		
	 </tr></table>
	 
	</section>
	
	<section>
	 <table><tr>
	 	<td style="width:150px; background-color:#d7dbdd"><h4>Crear una nueva colección de imágenes SVG</h4></td>
		<td style="width:600px">
			<form id="CrearColeccion" method="GET" action="/GestorSvg/apiCC">
				<table><tr>
					<td>Introducir nombre de la colección:</td>
					<td><input required name="collection"></td>
				</tr></table>
			
			<hr>
			<button type="submit" form="CrearColeccion">Crear coleccion</button>
			</form>
		</td>
	</tr></table>
	</section>
	<section>
	  <table><tr>
	  	<td style="width:150px; background-color:#d7dbdd"><h4>Crear una nueva imagen SVG (en blanco) en una colección</h4></td>
		<td style="width:600px">
			<form id="ImagenNueva" method="GET" action="/GestorSvg/apiNI">
				<table><tr>
					<td>Nombre de la nueva imagen SVG:</td>
					<td><input required name="svgName"></td>
				</tr><tr>
					<td>Colección destino de la imagen</td>
					<td><input required name="collection"></td>
				</tr></table>
			
			<hr>
			<button id="submit" form="ImagenNueva">Nueva imagen</button>
			</form>
		</td>
	</tr></table>
	</section>

	 
   <script>
        function leerArchivo() {
            var fileInput = document.getElementById('fileInput');
            var file = fileInput.files[0];
            var reader = new FileReader();
            reader.onload = function(e) {
                var contenido = e.target.result;
                document.getElementById('contenidoArchivo').value = contenido;
            };
            reader.readAsText(file);
        }
    </script>
	 
		

	<section>
	 <table><tr>
	 	<td style="width:150px; background-color:#d7dbdd"><h4>Borrar una colección de imagenes SVG</h4></td>
		<td style="width:600px">
			<form id="BorrarColeccion" method="GET" action="/GestorSvg/apiDC">
				<table><tr>
					<td>Introducir nombre de la colección:</td>
					<td><input  required name="collection"></td>
				</tr></table>
			<hr>
			<button form="BorrarColeccion">Borrar colección</button>
			</form>
		</td>
	</tr></table>
	</section>
	
	 <section>
	  <table><tr>
	  	<td style="width:150px; background-color:#d7dbdd"><h4>Sube una imagen SVG desde un archivo a un colección</h4></td>
		<td style="width:600px">
	
				<input type="file" id="fileInput" accept=".svg" /> 
    			<button onclick="leerArchivo()">Leer Archivo</button>
    		
    		<hr>
    		<form id="ImagenFichero" method="POST" action="/GestorSvg/apiNIF">
  				<input type="hidden"id="contenidoArchivo" required name="imagenSVG">		
				<table><tr>
					<td>Nombre de la nueva imagen SVG:</td>
					<td><input id="nombreArchivo" required name="svgName"></td>	
				</tr><tr>
					<td>Colección destino de la imagen</td>
					<td><input required name="collection"></td>
				</tr></table>
				<hr>
				<button id="submit" form="ImagenFichero">Subir imagen</button>
			</form>
		</td>
	</tr></table>
	</section>

	<footer><h5>Sistemas Web - Escuela Ingeniería de Bilbao</h5></footer>
</body>
</html>
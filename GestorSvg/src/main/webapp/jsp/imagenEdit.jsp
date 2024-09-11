<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>
<%@ page import="java.util.*" %>
<%@ page import="org.w3c.dom.NodeList" %>
<%String collection = (String) request.getAttribute("collection");
    String svgName = (String) request.getAttribute("svgName");
    String imagenSVG = (String) request.getAttribute("imagenSVG");
    String imagenURI = (String) request.getAttribute("imagenURI");
    System.out.print("Ennnnnn ImagenEditJSP" + imagenSVG);
%>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="pragma" content="no-cache">
    <meta http-equiv="expires" content="0">
    <meta charset="utf-8">
    <title>Edición SVG</title>
    <link href="/GestorSvg/css/styleSheet.css" rel="stylesheet"/>
</head>
<body>
<header>
    <h1>Gestor Imágenes SVG en eXist - SW-2023</h1>
    <h3>Edición de la imagen: <%=svgName%></h3>
</header>

<nav class="menu">
    <a href="./jsp/index.jsp">Inicio</a>
    <a onclick="document.getElementById('myform').submit();">Atras</a>
</nav>
<form id="myform" method="POST" action="./apiLR">
    <input type="hidden" name="collection" value="<%=collection%>" />
</form>

<table  style="width:100%" class="edicion">
    <tr class="edicion">
        <th class="edicion">Imagen Original</th>
        <th  class="edicion">Imagen Modificada</th>
        <th class="edicion">SRC</th>
    </tr>
    <script>
        function loadCatPicture() {
            var img = document.getElementById('imuri');
            img.src = img.src.split("?")[0] + '?ver=' + (new Date().getTime());
        };

        window.onload = function() {
            loadCatPicture();
        };
    </script>
    <tr class="edicion">
        <td class="edicion"><img id="imuri" class="edicion"
                                 src="<%=imagenURI%>" /></td>
        <td class="edicion"><%=imagenSVG%></td>
        <td class="edicion">
            <form id="formulario" method='post' action="./appSaveUpdate">
                    <%="<input type='hidden' name='collection' value='" + collection + "'/>"%>
                    <%="<input type='hidden' name='svgName' value='" + svgName + "'/>"%>
                <textarea  class="input-field" name='imagenSVG' wrap="soft" id="textareaSVG"
                           contenteditable="true" rows="20" cols="80"><%=imagenSVG%></textarea>
        </td>
    </tr>
</table>

<nav class="menu">
    <label for="opciones"></label> <select id="opciones"
                                           name="actualizar_salva" form="formulario">
    <option value="update">Actualizar</option>
    <option value="save">Guardar</option>
</select>
    <button type='submit' form="formulario" onclick=loadCatPicture()>Actualizar/Guardar</button>
</nav>
<footer><h5>Sistemas Web - Escuela Ingeniería de Bilbao</h5></footer>
</body>
</html>
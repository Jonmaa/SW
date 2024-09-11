<!DOCTYPE html>
<%@ page import="java.util.*,helper.info.*" %>
<%  ArrayList<MessageInfo> messageList = (ArrayList) request.getAttribute("messageList");
    ServletContext context = request.getServletContext();
    HashMap<String, String> loggedinUsers = (HashMap) context.getAttribute("loggedin_users");
//HttpSession sesion=request.getSession();
%>
<%@ page contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>

<html lang="es">
<head>
    <title>Visor de Mensajes</title>
    <link href="/ShareInfo/css/styleSheet.css" rel="stylesheet"/>
    <script src="/ShareInfo/js/GetTime.js"></script>
    <script src="/ShareInfo/js/GetMsg.js"></script>
    <script src="/ShareInfo/js/GetUsers.js"></script>
</head>

<body onload="GetTimeIO();GetMsg();GetUsers()">
<header>
    <h1>Web para Compartir Mensajes Cortos</h1>
    <h3>Vista de Mensasjes</h3>
</header>

<section>
    <a href="/ShareInfo/servlet/MainServlet">Actualizar</a>
    <a href="/ShareInfo/servlet/ExitServlet"> Exit</a>
</section>

<section>
    Mi usuario: <%=session.getAttribute("username") %>
</section>

<section class="ActiveUsers">
    Usuarios Activos:
    <% for (Map.Entry<String, String> entry : loggedinUsers.entrySet()) { %>
        <%=entry.getKey()%>
    <% } %>
</section>

<section>
    <form method="POST" accept-charset=utf-8 action="/ShareInfo/servlet/MainServlet">
        <table>
            <tr>
                <td>Mensaje:</td>
                <td><textarea name="message" id="message"></textarea></td>
            </tr>
        </table>
        <button>Enviar</button>
    </form>
</section>

<section>
    <table class="msgtable">
        <tr>
            <th>Usuario</th>
            <th>Mensaje</th>
        </tr>
        <%  for (MessageInfo messageInfo : messageList){ %>
        <tr>
        
            <td><%=messageInfo.getUsername()%></td>
            <td><%=messageInfo.getMessage()%> </td>
        </tr>
        <% } %>
    </table>
</section>

<footer><p>
    <h2>Hora Servidor:
        <span class="hour">0</span>:<span class="minute">0</span>:<span class="second">0</span>
    </h2><h2>
        Hora Cliente:
        <span class="hcliente">0</span>
    </h2>
</footer>

<footer>Sistemas Web - Escuela de Ingenieria de Bilbao</footer>
</body>
</html>
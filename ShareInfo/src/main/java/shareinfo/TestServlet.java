package shareinfo;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import helper.db.*;
import helper.info.MessageInfo;

public class TestServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private MySQLdb mySQLdb;

	public void init(ServletConfig config) {
		System.out.println("---> init() de TestServlet");
		mySQLdb = new MySQLdb();
		System.out.println("<--- init() de TestServlet");
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		System.out.println("---> doGet() de TestServlet");
		PrintWriter http_out = response.getWriter(); // clase para escribir contenido respuesta

		String type = request.getParameter("type"); // leemos el parámetro tipo de la respuesta
		System.out.println("---- type: " + type);

		// registerUser
		// localhost:8080/ShareInfo/servlet/TestServlet?type=registerUser&email=123@123.com&password=123&username=123
		if (type != null) {
			if (type.equals("registerUser")) {
				System.out.println("---- Solicitado registrar un usuario");
				String email = request.getParameter("email");
				String password = request.getParameter("password");
				String username = request.getParameter("username");
				if (email != null && password != null && username != null) {
					mySQLdb.setUserInfo(email, password, username);
					http_out.println("El almacenamiento de datos se ha realizado correctamente: Usuario registrado");
				} else {
					http_out.println("No se han enviado bien los parámetros");
				}
			}
			// getUsername
			// localhost:8080/ShareInfo/servlet/TestServlet?type=getUsername&email=123@123.com&password=123
			if (type.equals("getUsername")) {
				System.out.println("---- Obtener Username");
				String email = request.getParameter("email");
				String password = request.getParameter("password");
				String username;
				if (email != null && password != null) {
					username = mySQLdb.getUsername(email, password);
					http_out.println("El nombre de usuario es: " + username);
				} else {
					http_out.println("No se han enviado bien los parámetros");
				}
			}
			// registerMessage
			// localhost:8080/ShareInfo/servlet/TestServlet?type=registerMessage&message=hola de 123$&username=123
			if (type.equals("registerMessage")) {
				System.out.println("---- Solicitado registrar mensaje");
				String message = request.getParameter("message");
				String username = request.getParameter("username");
				if (message != null && username != null) {
					mySQLdb.setMessageInfo(message, username);
					http_out.println("El almacenamiento de datos se ha realizado correctamente: mensaje registrado");
				} else {
					http_out.println("No se han enviado bien los parámetros");
				}
			}
			// getMessage
			// localhost:8080/ShareInfo/servlet/TestServlet?type=getMessages&format=json
			// localhost:8080/ShareInfo/servlet/TestServlet?type=getMessages&format=html
			if (type.equals("getMessages")) {
				System.out.println("---- Solicitado obtener mensajes");
				String format = request.getParameter("format");
				if (format != null) {
					if (format.equals("json")) {
						System.out.println("---- Parametros: " + format);

						ArrayList<MessageInfo> messageList = mySQLdb.getAllMessages();
						Gson gson = new Gson();
						String json = gson.toJson(messageList);
						System.out.println(json);
						http_out.println(json);
					}
					if (format.equals("html")) {
						System.out.println("---- Parametros: " + format);

						ArrayList<MessageInfo> messageList = mySQLdb.getAllMessages();
						request.setAttribute("messageList", messageList);

						System.out.println("     Redireccionando el usuario a viewMessages.jsp");
						RequestDispatcher rd = request.getRequestDispatcher("/jsp/listaMensajes.jsp");
						rd.forward(request, response);
					}
				} else {
					http_out.println("No se han enviado bien el parametro format");
				}
			}

		} else {
			http_out.println("No se han enviado el parámetro type");

		}
		System.out.println("<--- doPost() de TestServlet");
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		System.out.println("---> doPost() de TestServlet");
		doGet(request, response);
	}

}

package shareinfo;

import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

import helper.db.*;

public class LoginServlet extends HttpServlet{

	private static final long serialVersionUID = 1L;
	private MySQLdb mySQLdb;
	private int numconexiones=0;
	private int numconexionesOK=0;
	
	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de LoginServlet");
		mySQLdb = new MySQLdb();
		System.out.println("---> Saliendo de init() de LoginServlet");
	}
	public void destroy() {
		System.out.println("---> Entrando en destroy()de LoginServlet");
		System.out.println("     Conexiones: " + numconexiones);
		System.out.println("     Conexiones OK: "+ numconexionesOK);
		System.out.println("---> Saliendo de destry() de LoginServlet");
	}
		
    public void doPost(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
    	System.out.println("---> Entrando en doPost() de LoginServlet");
    	
    	String email = request.getParameter("email");
		String password = request.getParameter("password");
		System.out.println("     Estrayendo parámetros de la petición: " + email + " " + password);
		
		numconexiones=numconexiones+ 1;
		
		String username = mySQLdb.getUsername(email, password);
		
		if(username == null) {
			System.out.println("     Login error: redireccionando al usuarioa a loginForm.html");
			
			request.setAttribute("error", "usuario o contraseña incorrectos");
			RequestDispatcher rd = request.getRequestDispatcher("/jsp/loginForm.jsp");
			rd.forward(request, response);
			
		} else {
			numconexionesOK=numconexionesOK+1;
			HttpSession session = request.getSession(true);
			session.setMaxInactiveInterval(120);
			String sessionID = session.getId();
			System.out.println("     Sesion de Usuario para " + username + ": " + sessionID);
			session.setAttribute("username", username);
			long sessionTime = session.getCreationTime();
			System.out.println("     Sesion Time: " + sessionTime);
			
			// CONTEXTO Lista de usuarios
			
			System.out.println("     Cogiendo la lista de usuarios activos de contexto: ");
			ServletContext context = request.getServletContext();
			HashMap<String, String> loggedinUsers = (HashMap) context.getAttribute("loggedin_users");
			if(loggedinUsers == null) {
				System.out.println("Lista vacia");
				loggedinUsers = new HashMap();
				loggedinUsers.put(username, sessionID);
			} else {
				if(!loggedinUsers.containsKey(username)) {
					System.out.println(username + " no esta en la lista");
					loggedinUsers.put(username, sessionID);
				} else {
					System.out.println(username + " ya esta en la lista");
				}
			}
			context.setAttribute("loggedin_users", loggedinUsers);
			
			
			System.out.println("     Loggedin users: " + loggedinUsers.toString());
			System.out.println("     Redireccionar al usuario al MainServlet");
			RequestDispatcher rd = context.getNamedDispatcher("MainServlet");
			rd.forward(request, response);
		}
		
		System.out.println("---> Saliendo de doPost() en LoginServlet");
    }
}


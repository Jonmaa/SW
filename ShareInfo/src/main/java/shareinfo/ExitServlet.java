package shareinfo;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;


public class ExitServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
     public ExitServlet() {
        super();
     
    }
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		HttpSession sesion= request.getSession();
		sesion.invalidate();
		
		request.setAttribute("error","sesión cerrada por ususario");
		RequestDispatcher rd = request.getRequestDispatcher("/jsp/loginForm.jsp");
		rd.forward(request, response);
		
	}

}

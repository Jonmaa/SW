package servlets;

import HTTPeXist.HTTPeXist;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class CreateCollection extends HttpServlet {

    private HTTPeXist eXist = new HTTPeXist("http://localHost:8080");

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String collection = "";
        collection = request.getParameter("collection");
        int data = 0;
        data = eXist.create(collection);

        if (data != 200) {
            request.setAttribute("informacion", "Coleccion No Creada");
            RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
            rd.forward(request, response);
        } else {
            request.setAttribute("informacion", "Coleccion Creada");
            RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
            rd.forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doGet(request, response);
    }

}

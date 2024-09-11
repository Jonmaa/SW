package servlets;

import HTTPeXist.HTTPeXist;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class NewImage extends HttpServlet {

    private HTTPeXist eXist = new HTTPeXist("http://localHost:8080");

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String collection = "";
        collection = request.getParameter("collection");
        int data = 0;
        String name = request.getParameter("svgName");
        data = eXist.subirString(collection, "", name);

        if (data != 201) {
            request.setAttribute("informacion", "Nueva imagen no creada");
            RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
            rd.forward(request, response);
        } else {
            request.setAttribute("informacion", "Nueva imagen creada");
            RequestDispatcher rd = request.getRequestDispatcher("/jsp/imagenEdit.jsp");
            request.setAttribute("svgName", name);
            request.setAttribute("collection", collection);
            request.setAttribute("imagenSVG", "");
            request.setAttribute("imagenURI", "http://localhost:8080/exist/rest/db/" + collection + "/" + name + "/");
            rd.forward(request, response);
        }
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        doGet(request, response);
    }
}

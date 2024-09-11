package servlets;

import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import HTTPeXist.HTTPeXist;

public class DeleteSvg extends HttpServlet {

    private static final long serialVersionUID = 1L;
    private HTTPeXist eXist;


    public void init(ServletConfig config) {
        System.out.println("---> Entrando en init()de listResource");
        eXist = new HTTPeXist("http://localHost:8080");
        System.out.println("---> Saliendo de init()de LoginServlet");
    }

    //metodo doGet para eliminar un recurso
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String collection = "";
        collection = request.getParameter("collection");
        String resourceName = "";
        resourceName = request.getParameter("svgName");
        eXist.delete(collection, resourceName);
        request.setAttribute("informacion", "Imagen borrada");
        RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
        rd.forward(request, response);


    }
}

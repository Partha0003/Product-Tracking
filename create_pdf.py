import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Top of page)
        self.drawString(36, 808, "Supply Chain Product Tracking System  |  Placement Interview Preparation Guide")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 802, 559, 802)
        
        # Footer (Bottom of page)
        self.line(36, 30, 559, 30)
        self.drawString(36, 20, "Confidential  |  Prepared for IT Technical Interviews (TCS, CTS, Infosys, Wipro, LTIMindtree)")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 20, page_str)
        self.restoreState()

def build_pdf(filename="Supply_Chain_Project_Interview_Preparation.pdf"):
    # Target exactly 7 pages. A4 = 595.27 x 841.89 pt. Margin: 36pt. Usable width: 523pt.
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Deep Navy
    SECONDARY = colors.HexColor("#0D9488")  # Teal
    DARK_TEXT = colors.HexColor("#0F172A")  # Slate 900
    MUTED_TEXT = colors.HexColor("#475569") # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Slate 50
    CARD_BG = colors.HexColor("#F1F5F9")    # Slate 100
    ACCENT_BG = colors.HexColor("#EFF6FF")  # Blue 50
    BORDER_COLOR = colors.HexColor("#CBD5E1")

    # Typography Styles
    style_page_title = ParagraphStyle(
        'PageTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=PRIMARY,
        spaceAfter=3
    )

    style_page_subtitle = ParagraphStyle(
        'PageSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=MUTED_TEXT,
        spaceAfter=6
    )

    style_h2 = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12.5,
        textColor=PRIMARY,
        spaceBefore=4,
        spaceAfter=2
    )

    style_h3 = ParagraphStyle(
        'Heading3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=SECONDARY,
        spaceBefore=3,
        spaceAfter=1
    )

    style_body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
        textColor=DARK_TEXT,
        spaceAfter=2
    )

    style_body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=DARK_TEXT
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=DARK_TEXT
    )

    style_qa_box = ParagraphStyle(
        'QABox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=DARK_TEXT
    )

    def make_card(title, content_list, bg_color=CARD_BG, border_color=BORDER_COLOR):
        elements = []
        if title:
            elements.append(Paragraph(f"<b>{title}</b>", style_h3))
        for item in content_list:
            if isinstance(item, str):
                elements.append(Paragraph(item, style_callout))
            else:
                elements.append(item)
        table = Table([[elements]], colWidths=[523])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        return table

    story = []

    # =========================================================================
    # PAGE 1: PROJECT INTRODUCTION & HOW TO PITCH
    # =========================================================================
    story.append(Paragraph("PAGE 1 - Project Introduction & How to Pitch", style_page_title))
    story.append(Paragraph("Master the initial 2 minutes of your technical placement interview with tailored elevator pitches.", style_page_subtitle))

    # Overview Table
    overview_data = [
        [Paragraph("<b>Project Name</b>", style_body_bold), Paragraph("Supply Chain Product Tracking System", style_body)],
        [Paragraph("<b>Problem Statement</b>", style_body_bold), Paragraph("Traditional logistics lack centralized, real-time visibility. Tracking shipments across production and distribution causes dispatch delays, misplaced goods, and untraceable supply chain status.", style_body)],
        [Paragraph("<b>Main Objective</b>", style_body_bold), Paragraph("Develop an enterprise RESTful backend service to register products and record their strict milestone transitions (<b>Manufactured -&gt; Shipped -&gt; Delivered</b>) with zero data loss.", style_body)],
        [Paragraph("<b>Real-World Application</b>", style_body_bold), Paragraph("Manufacturing hubs, e-commerce order fulfillment centers, and third-party logistics (3PL) warehouse networks.", style_body)],
        [Paragraph("<b>Target Users</b>", style_body_bold), Paragraph("Plant warehouse managers, inventory officers, logistics dispatch coordinators.", style_body)],
        [Paragraph("<b>Core Tech Stack</b>", style_body_bold), Paragraph("<b>Java 21, Spring Boot 3.3.5</b> (Spring Web, Spring Data JPA, Hibernate), <b>PostgreSQL</b>, Apache Maven, Jakarta Validation.", style_body)],
    ]
    t_overview = Table(overview_data, colWidths=[115, 408])
    t_overview.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_overview)
    story.append(Spacer(1, 4))

    story.append(Paragraph("How to Explain This Project in an Interview (Choose Your Version)", style_h2))

    # 3 Pitches
    pitch_30 = (
        "<b>30-Second Elevator Pitch:</b><br/>"
        "<i>\"In my final semester, I developed a <b>Supply Chain Product Tracking System</b> using <b>Java 21, Spring Boot 3, and PostgreSQL</b>. "
        "The application provides RESTful APIs to track products across critical supply chain stages-from Manufacturing to Shipping and Delivery. "
        "I built the complete layered backend architecture consisting of Controllers, Services, and Spring Data JPA Repositories to ensure thread-safe, robust data persistence.\"</i>"
    )
    story.append(make_card("1. The 30-Second Quick Pitch (When asked: 'Briefly introduce your project')", [pitch_30], ACCENT_BG, colors.HexColor("#93C5FD")))
    story.append(Spacer(1, 4))

    pitch_60 = (
        "<b>1-Minute Pitch: Problem, Solution, Tech & Features:</b><br/>"
        "<i>\"In traditional logistics, tracking item movement across multiple checkpoints often suffers from manual errors and data discrepancies. "
        "To solve this, I built a centralized <b>Supply Chain Product Tracking backend using Spring Boot and PostgreSQL</b>.<br/>"
        "The system exposes 5 key REST endpoints: registering new products with automated default statuses, viewing all inventory, updating milestone stages, and removing discontinued items. "
        "I used <b>Spring Data JPA with Hibernate</b> for database operations and structured the application into clean Controllers, Business Services, DTOs with Jakarta validation, and a Global Exception Handler. "
        "This project originally started in Node.js, and I migrated it to Spring Boot to leverage enterprise-level typing, maintainability, and clean 3-tier architecture.\"</i>"
    )
    story.append(make_card("2. The 1-Minute Pitch (Standard answer for 'Tell me about your project')", [pitch_60], CARD_BG, BORDER_COLOR))
    story.append(Spacer(1, 4))

    pitch_120 = (
        "<b>2-Minute Pitch: Comprehensive Architecture & Workflow:</b><br/>"
        "<i>\"My project is a <b>Supply Chain Product Tracking System</b> engineered with <b>Spring Boot 3 and PostgreSQL</b>. "
        "The core business challenge is providing real-time lifecycle tracking of physical goods as they move from factory production to end delivery.<br/>"
        "<b>Architecture:</b> I followed a strict 3-tier enterprise architecture. When an HTTP request arrives, it hits my <b>ProductController</b>, where incoming JSON is validated using DTOs and Jakarta annotations like <code>@NotBlank</code>. "
        "The controller delegates execution to <b>ProductServiceImpl</b>, which encapsulates the business rules-such as ensuring a new product defaults to 'Manufactured' and guaranteeing that status updates never accidentally overwrite the product's name or origin.<br/>"
        "<b>Data Layer:</b> The service communicates with PostgreSQL via <b>ProductRepository</b> extending Spring Data's <code>JpaRepository</code>. In PostgreSQL, products are mapped using a JPA Entity with an auto-incrementing identity ID.<br/>"
        "<b>Migration Experience:</b> A key technical highlight was migrating the backend from Node.js/Express to Spring Boot while maintaining 100% API contract and database schema compatibility on port 5000.\"</i>"
    )
    story.append(make_card("3. The 2-Minute In-Depth Pitch (When the interviewer is a Senior Java Technical Lead)", [pitch_120], ACCENT_BG, colors.HexColor("#93C5FD")))
    story.append(Spacer(1, 4))

    # Interview Trainer Insight Table
    trainer_data = [
        [Paragraph("<b>Why did you choose this project?</b>", style_body_bold), Paragraph("Supply chain visibility is a mission-critical domain in enterprise IT. I wanted hands-on experience building scalable CRUD REST APIs with Spring Data JPA and relational databases.", style_body)],
        [Paragraph("<b>What was your individual role?</b>", style_body_bold), Paragraph("Sole backend developer. Designed the PostgreSQL schema, mapped JPA entities, coded all Controllers, DTOs, and Services, and configured database pooling in application.properties.", style_body)],
        [Paragraph("<b>Key learning & challenge faced?</b>", style_body_bold), Paragraph("Learned how Spring Boot auto-configuration and Hibernate simplify boilerplate JDBC code. A key challenge was ensuring that PUT status updates strictly modified only the status field without altering product origin.", style_body)],
    ]
    t_trainer = Table(trainer_data, colWidths=[135, 388])
    t_trainer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_trainer)

    # END OF PAGE 1
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ARCHITECTURE & WORKFLOW
    # =========================================================================
    story.append(Paragraph("PAGE 2 - Complete Project Architecture and Workflow", style_page_title))
    story.append(Paragraph("Understand the end-to-end internal flow from client request to PostgreSQL database persistence.", style_page_subtitle))

    story.append(Paragraph("1. High-Level 3-Tier Layered Architecture", style_h2))
    
    arch_data = [
        [Paragraph("<b>Layer</b>", style_body_bold), Paragraph("<b>Component in Project</b>", style_body_bold), Paragraph("<b>Core Responsibility</b>", style_body_bold)],
        [Paragraph("<b>1. Client / Frontend</b>", style_body), Paragraph("Browser / Postman / Client App", style_body), Paragraph("Sends JSON HTTP requests to <code>http://localhost:5000</code> and receives JSON responses.", style_body)],
        [Paragraph("<b>2. Controller Layer</b>", style_body), Paragraph("<code>RootController</code><br/><code>ProductController</code>", style_body), Paragraph("Entry point for HTTP requests. Handles URL mapping, path variables, request body deserialization, and validates DTOs.", style_body)],
        [Paragraph("<b>3. DTO Layer</b>", style_body), Paragraph("<code>ProductRequestDto</code><br/><code>StatusUpdateDto</code>", style_body), Paragraph("Decouples internal DB entities from external API payloads. Uses <code>@NotBlank</code> to validate input fields.", style_body)],
        [Paragraph("<b>4. Service Layer</b>", style_body), Paragraph("<code>ProductService</code> (Interface)<br/><code>ProductServiceImpl</code> (Class)", style_body), Paragraph("Encapsulates business logic, enforces defaults ('Manufactured'), and prevents accidental column mutations.", style_body)],
        [Paragraph("<b>5. Repository Layer</b>", style_body), Paragraph("<code>ProductRepository</code><br/>(extends <code>JpaRepository</code>)", style_body), Paragraph("Data access abstraction. Generates SQL queries dynamically for CRUD operations without raw SQL code.", style_body)],
        [Paragraph("<b>6. Entity Layer</b>", style_body), Paragraph("<code>Product.java</code>", style_body), Paragraph("JPA entity mapping the Java object to the PostgreSQL <code>products</code> table via Hibernate ORM.", style_body)],
        [Paragraph("<b>7. Database</b>", style_body), Paragraph("<b>PostgreSQL</b> (Port 5432)", style_body), Paragraph("Relational database storing persistent table rows with auto-incrementing <code>id SERIAL PRIMARY KEY</code>.", style_body)],
    ]
    t_arch = Table(arch_data, colWidths=[95, 128, 300])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(arch_data)):
        if i % 2 == 1:
            t_arch.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_arch)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Complete End-to-End Request Flow (Step-by-Step for All 5 Operations)", style_h2))

    flow_data = [
        [Paragraph("<b>Operation</b>", style_body_bold), Paragraph("<b>Endpoint & Method</b>", style_body_bold), Paragraph("<b>Internal Step-by-Step Execution Flow</b>", style_body_bold), Paragraph("<b>Response Code</b>", style_body_bold)],
        [
            Paragraph("<b>Health Check</b>", style_body),
            Paragraph("<code>GET /</code>", style_body),
            Paragraph("Client pings server -&gt; <code>RootController.healthCheck()</code> intercepts -&gt; Returns plain text string <code>\"Server is running!\"</code> directly without hitting DB.", style_body),
            Paragraph("<code>200 OK</code>", style_body)
        ],
        [
            Paragraph("<b>Register Product</b>", style_body),
            Paragraph("<code>POST /products</code>", style_body),
            Paragraph("1. Client sends JSON <code>{name, origin, status}</code>.<br/>2. <code>ProductController</code> validates <code>@Valid ProductRequestDto</code>.<br/>3. <code>ProductServiceImpl</code> sets status to 'Manufactured' if blank and builds <code>Product</code> entity.<br/>4. <code>ProductRepository.save(product)</code> executes PostgreSQL <code>INSERT</code>.<br/>5. Generated ID is assigned and saved entity returned as JSON.", style_body),
            Paragraph("<code>200 OK</code><br/>(JSON Product with ID)", style_body)
        ],
        [
            Paragraph("<b>View All Products</b>", style_body),
            Paragraph("<code>GET /products</code>", style_body),
            Paragraph("1. Client requests inventory.<br/>2. <code>ProductController</code> calls <code>productService.getAllProducts()</code>.<br/>3. <code>ProductRepository.findAll()</code> triggers <code>SELECT * FROM products</code>.<br/>4. Hibernate converts SQL result set into <code>List&lt;Product&gt;</code>.<br/>5. Controller serializes list into a JSON array.", style_body),
            Paragraph("<code>200 OK</code><br/>(JSON Array)", style_body)
        ],
        [
            Paragraph("<b>Update Status</b>", style_body),
            Paragraph("<code>PUT /products/{id}/status</code>", style_body),
            Paragraph("1. Client sends target ID in URL and JSON <code>{status: \"Shipped\"}</code> in body.<br/>2. <code>ProductServiceImpl.updateProductStatus()</code> searches product by ID using <code>findById(id)</code>.<br/>3. If not found, throws <code>ResourceNotFoundException</code> (404).<br/>4. If found, sets <b>ONLY</b> the new status, preserving original <code>name</code> and <code>origin</code>.<br/>5. Calls <code>save()</code> which executes SQL <code>UPDATE</code>.", style_body),
            Paragraph("<code>200 OK</code><br/>(Updated Product JSON)", style_body)
        ],
        [
            Paragraph("<b>Delete Product</b>", style_body),
            Paragraph("<code>DELETE /products/{id}</code>", style_body),
            Paragraph("1. Client sends ID.<br/>2. Service checks existence via <code>findById(id)</code> (throws 404 if missing).<br/>3. Calls <code>productRepository.delete(product)</code> which executes SQL <code>DELETE FROM products WHERE id = ?</code>.<br/>4. Controller returns JSON: <code>{\"message\": \"Product deleted successfully\"}</code>.", style_body),
            Paragraph("<code>200 OK</code><br/>(Confirmation JSON)", style_body)
        ],
    ]
    t_flow = Table(flow_data, colWidths=[70, 95, 290, 68])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(flow_data)):
        if i % 2 == 1:
            t_flow.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_flow)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. The Product Lifecycle & Logistics State Model", style_h2))
    lifecycle_text = (
        "<b>Milestone State Progression:</b> <code>[Manufactured]</code> -&gt; <code>[Shipped]</code> -&gt; <code>[Delivered]</code><br/>"
        "• <b>Manufactured:</b> Product has finished assembly at the factory/plant and is registered in the database.<br/>"
        "• <b>Shipped:</b> Product has been handed over to dispatch and is in transit across distribution channels.<br/>"
        "• <b>Delivered:</b> Product has reached the destination warehouse or customer doorstep.<br/>"
        "<b>Why is milestone status tracking important in Viva?</b> Interviewers love this because it reflects real-world supply chain visibility: preventing inventory loss, identifying transit bottlenecks, and providing accurate delivery estimates to stakeholders."
    )
    story.append(make_card(None, [lifecycle_text], CARD_BG, BORDER_COLOR))

    # END OF PAGE 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TECH STACK FOR VIVA
    # =========================================================================
    story.append(Paragraph("PAGE 3 - Technology Stack Explained for Viva", style_page_title))
    story.append(Paragraph("Comprehensive guide to each technology, real-world analogies, and core interview comparison questions.", style_page_subtitle))

    story.append(Paragraph("1. The 10 Core Technologies Deep Dive", style_h2))

    tech_data = [
        [Paragraph("<b>Technology</b>", style_body_bold), Paragraph("<b>What & Why Used in Project</b>", style_body_bold), Paragraph("<b>Interview Viva Question & Quick Answer</b>", style_body_bold)],
        [
            Paragraph("<b>Java 21</b>", style_body_bold),
            Paragraph("Modern LTS release providing high performance, enhanced pattern matching, record classes, and virtual threads.", style_body),
            Paragraph("<b>Q: Why use Java for enterprise backends?</b><br/><b>A:</b> Platform-independence, strong type safety, robust memory management, and rich enterprise ecosystem.", style_body)
        ],
        [
            Paragraph("<b>Spring Boot 3.x</b>", style_body_bold),
            Paragraph("Opinionated framework on top of Spring. Uses starter dependencies and auto-configuration to eliminate boilerplate XML.", style_body),
            Paragraph("<b>Q: What are key benefits of Spring Boot?</b><br/><b>A:</b> Embedded Tomcat server, auto-configuration, production metrics, and rapid development setup.", style_body)
        ],
        [
            Paragraph("<b>Spring MVC</b>", style_body_bold),
            Paragraph("Model-View-Controller module in Spring. Handles incoming HTTP requests via <code>DispatcherServlet</code> and routes them to Controller methods.", style_body),
            Paragraph("<b>Q: What is the role of DispatcherServlet?</b><br/><b>A:</b> It is the front controller that intercepts all incoming HTTP requests and routes them to appropriate handlers.", style_body)
        ],
        [
            Paragraph("<b>REST API</b>", style_body_bold),
            Paragraph("Architectural style using standard HTTP verbs (GET, POST, PUT, DELETE) and JSON for stateless client-server communication.", style_body),
            Paragraph("<b>Q: What does 'stateless' mean in REST?</b><br/><b>A:</b> The server stores no client session context between requests; each request contains all info required to process it.", style_body)
        ],
        [
            Paragraph("<b>Spring Data JPA</b>", style_body_bold),
            Paragraph("Data access abstraction layer that eliminates boilerplate DAO code by providing interfaces like <code>JpaRepository</code> with auto-implemented CRUD.", style_body),
            Paragraph("<b>Q: How does JpaRepository work without implementation?</b><br/><b>A:</b> Spring dynamically creates proxy implementations at runtime based on method names and JPA conventions.", style_body)
        ],
        [
            Paragraph("<b>Hibernate</b>", style_body_bold),
            Paragraph("Leading Object-Relational Mapping (ORM) provider implementing the JPA standard. Automatically translates Java objects into SQL queries.", style_body),
            Paragraph("<b>Q: What problem does an ORM solve?</b><br/><b>A:</b> Bridges the object-relational impedance mismatch between object-oriented Java classes and relational SQL tables.", style_body)
        ],
        [
            Paragraph("<b>PostgreSQL</b>", style_body_bold),
            Paragraph("Powerful open-source relational database known for ACID compliance, reliability, and robust support for concurrent transactions.", style_body),
            Paragraph("<b>Q: What ensures data reliability in PostgreSQL?</b><br/><b>A:</b> Strict ACID compliance (Atomicity, Consistency, Isolation, Durability) and write-ahead logging (WAL).", style_body)
        ],
        [
            Paragraph("<b>Apache Maven</b>", style_body_bold),
            Paragraph("Build automation and dependency management tool using <code>pom.xml</code>. Handles library downloads, compilation, packaging, and testing.", style_body),
            Paragraph("<b>Q: What is the Maven build lifecycle?</b><br/><b>A:</b> A sequence of phases: <code>validate -&gt; compile -&gt; test -&gt; package -&gt; verify -&gt; install -&gt; deploy</code>.", style_body)
        ],
        [
            Paragraph("<b>PostgreSQL JDBC Driver</b>", style_body_bold),
            Paragraph("Database adapter library allowing Java applications to communicate with PostgreSQL over TCP/IP using standard JDBC APIs.", style_body),
            Paragraph("<b>Q: What happens if JDBC driver is missing?</b><br/><b>A:</b> Java cannot establish a raw socket connection to the database, throwing <code>ClassNotFoundException</code>.", style_body)
        ],
        [
            Paragraph("<b>JSON</b>", style_body_bold),
            Paragraph("JavaScript Object Notation: lightweight, human-readable text format used for data exchange between client and backend REST endpoints.", style_body),
            Paragraph("<b>Q: How does Spring Boot parse JSON?</b><br/><b>A:</b> It uses the <b>Jackson</b> library by default to serialize Java objects to JSON and deserialize JSON to DTOs.", style_body)
        ],
    ]
    t_tech = Table(tech_data, colWidths=[80, 213, 230])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(tech_data)):
        if i % 2 == 1:
            t_tech.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_tech)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Top 7 Interview Comparison Questions (Frequently Asked in Service Companies)", style_h2))

    comparisons = [
        [Paragraph("<b>Comparison</b>", style_body_bold), Paragraph("<b>Key Distinctions to Explain in Viva</b>", style_body_bold)],
        [
            Paragraph("<b>Spring vs Spring Boot</b>", style_body),
            Paragraph("<b>Spring</b> is a complete Java EE enterprise framework requiring extensive XML/Java configuration and manual server deployment. <b>Spring Boot</b> is an opinionated extension of Spring that provides starter dependencies, auto-configuration, and an embedded Tomcat server for immediate out-of-the-box execution.", style_body)
        ],
        [
            Paragraph("<b>Spring Boot vs Spring MVC</b>", style_body),
            Paragraph("<b>Spring MVC</b> is a specific web framework within Spring for building web applications and REST APIs using DispatcherServlet. <b>Spring Boot</b> is an umbrella project that packages Spring MVC along with automated setup, configuration, and runtime dependencies.", style_body)
        ],
        [
            Paragraph("<b>JPA vs Hibernate</b>", style_body),
            Paragraph("<b>JPA</b> (Jakarta Persistence API) is a standard Java <i>specification</i> or interface defining ORM rules. <b>Hibernate</b> is the actual concrete <i>implementation</i> that executes those rules and generates the underlying SQL statements.", style_body)
        ],
        [
            Paragraph("<b>JDBC vs JPA</b>", style_body),
            Paragraph("<b>JDBC</b> is low-level and requires manual SQL strings, opening/closing connections, and mapping <code>ResultSet</code> rows manually. <b>JPA</b> is high-level; it operates directly on Java objects (Entities) and handles SQL generation and object mapping automatically.", style_body)
        ],
        [
            Paragraph("<b>SQL vs PostgreSQL</b>", style_body),
            Paragraph("<b>SQL</b> is the universal standard query language for relational databases. <b>PostgreSQL</b> is a specific Relational Database Management System (RDBMS) software that executes SQL statements and stores data on disk.", style_body)
        ],
        [
            Paragraph("<b>Maven vs npm</b>", style_body),
            Paragraph("<b>Maven</b> is the build and dependency manager for Java projects using <code>pom.xml</code>. <b>npm</b> is the package manager for JavaScript/Node.js projects using <code>package.json</code>. When migrating this project, Maven replaced npm.", style_body)
        ],
        [
            Paragraph("<b>REST API vs Traditional Web App</b>", style_body),
            Paragraph("<b>Traditional web apps</b> render HTML pages on the server (JSP, Thymeleaf) and send full markup to the browser. A <b>REST API</b> sends raw data (JSON), allowing any client (React, Vue, mobile apps, IoT sensors) to consume it independently.", style_body)
        ],
    ]
    t_comp = Table(comparisons, colWidths=[120, 403])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(comparisons)):
        if i % 2 == 1:
            t_comp.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_comp)

    # END OF PAGE 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: PROJECT IMPLEMENTATION & CODE CONCEPTS
    # =========================================================================
    story.append(Paragraph("PAGE 4 - Project Implementation & Important Code Concepts", style_page_title))
    story.append(Paragraph("Codebase walkthrough, core Spring Boot annotations, and architectural separation of concerns.", style_page_subtitle))

    story.append(Paragraph("1. Codebase Structure & File Responsibilities", style_h2))

    files_data = [
        [Paragraph("<b>File / Class Name</b>", style_body_bold), Paragraph("<b>Package / Path</b>", style_body_bold), Paragraph("<b>Actual Code Responsibility in this Project</b>", style_body_bold)],
        [Paragraph("<code>ProductTrackingApplication.java</code>", style_body), Paragraph("<code>com.producttracking</code>", style_body), Paragraph("Main entry point containing <code>main()</code> method with <code>SpringApplication.run()</code>.", style_body)],
        [Paragraph("<code>Product.java</code>", style_body), Paragraph("<code>com.producttracking.entity</code>", style_body), Paragraph("JPA Entity mapped to table <code>products</code> with fields <code>id</code>, <code>name</code>, <code>origin</code>, and <code>status</code>.", style_body)],
        [Paragraph("<code>ProductRepository.java</code>", style_body), Paragraph("<code>com.producttracking.repository</code>", style_body), Paragraph("Interface extending <code>JpaRepository&lt;Product, Long&gt;</code> for built-in database CRUD operations.", style_body)],
        [Paragraph("<code>ProductService.java</code>", style_body), Paragraph("<code>com.producttracking.service</code>", style_body), Paragraph("Business interface defining contract methods (<code>getAllProducts</code>, <code>createProduct</code>, etc.).", style_body)],
        [Paragraph("<code>ProductServiceImpl.java</code>", style_body), Paragraph("<code>com.producttracking.service.impl</code>", style_body), Paragraph("Implements business logic: enforces defaults and ensures status updates protect name/origin.", style_body)],
        [Paragraph("<code>ProductController.java</code>", style_body), Paragraph("<code>com.producttracking.controller</code>", style_body), Paragraph("REST Controller handling <code>/products</code> routing, DTO validation, and returning <code>ResponseEntity</code>.", style_body)],
        [Paragraph("<code>RootController.java</code>", style_body), Paragraph("<code>com.producttracking.controller</code>", style_body), Paragraph("Handles <code>GET /</code> health check returning plain text <code>\"Server is running!\"</code>.", style_body)],
        [Paragraph("<code>ProductRequestDto.java</code>", style_body), Paragraph("<code>com.producttracking.dto</code>", style_body), Paragraph("DTO carrying input data for product creation with <code>@NotBlank</code> validations on name and origin.", style_body)],
        [Paragraph("<code>StatusUpdateDto.java</code>", style_body), Paragraph("<code>com.producttracking.dto</code>", style_body), Paragraph("DTO carrying payload for status changes with <code>@NotBlank</code> validation on status.", style_body)],
        [Paragraph("<code>CorsConfig.java</code>", style_body), Paragraph("<code>com.producttracking.config</code>", style_body), Paragraph("Implements <code>WebMvcConfigurer</code> allowing frontend origins to access APIs on port 5000.", style_body)],
        [Paragraph("<code>application.properties</code>", style_body), Paragraph("<code>src/main/resources</code>", style_body), Paragraph("Configures port 5000, PostgreSQL datasource URL, DB credentials, and Hibernate DDL update.", style_body)],
    ]
    t_files = Table(files_data, colWidths=[130, 115, 278])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(files_data)):
        if i % 2 == 1:
            t_files.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_files)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Spring Boot Annotations Demystified for Interviews", style_h2))

    annos_data = [
        [Paragraph("<b>Annotation</b>", style_body_bold), Paragraph("<b>Meaning & Why Used</b>", style_body_bold), Paragraph("<b>Where It Appears in Project</b>", style_body_bold)],
        [Paragraph("<code>@SpringBootApplication</code>", style_body), Paragraph("Enables auto-configuration, component scanning, and property support. Combines <code>@Configuration</code>, <code>@EnableAutoConfiguration</code>, and <code>@ComponentScan</code>.", style_body), Paragraph("<code>ProductTrackingApplication.java</code>", style_body)],
        [Paragraph("<code>@RestController</code>", style_body), Paragraph("Marks class as a REST endpoint handler. Combines <code>@Controller</code> and <code>@ResponseBody</code>, ensuring returned objects serialize directly to JSON.", style_body), Paragraph("<code>ProductController</code>, <code>RootController</code>", style_body)],
        [Paragraph("<code>@RequestMapping</code>", style_body), Paragraph("Sets base URL path mapping for all handler methods within the controller class.", style_body), Paragraph("<code>@RequestMapping(\"/products\")</code>", style_body)],
        [Paragraph("<code>@GetMapping, @PostMapping</code><br/><code>@PutMapping, @DeleteMapping</code>", style_body), Paragraph("Composed shortcut annotations mapping specific HTTP GET, POST, PUT, and DELETE methods to specific controller handler functions.", style_body), Paragraph("All endpoints inside <code>ProductController</code>", style_body)],
        [Paragraph("<code>@Service / @Repository</code>", style_body), Paragraph("Specialized <code>@Component</code> stereotypes indicating business service layer and database DAO access layer respectively. Enables Spring IoC component scanning.", style_body), Paragraph("<code>ProductServiceImpl.java</code><br/><code>ProductRepository.java</code>", style_body)],
        [Paragraph("<code>@Entity / @Table</code>", style_body), Paragraph("Specifies that the Java class is a persistent JPA entity mapped to the PostgreSQL table named <code>products</code>.", style_body), Paragraph("<code>Product.java</code>", style_body)],
        [Paragraph("<code>@Id / @GeneratedValue</code>", style_body), Paragraph("Marks primary key field. <code>GenerationType.IDENTITY</code> leverages PostgreSQL's native auto-incrementing <code>SERIAL</code> sequence.", style_body), Paragraph("<code>id</code> field in <code>Product.java</code>", style_body)],
        [Paragraph("<code>@RequestBody / @PathVariable</code>", style_body), Paragraph("<code>@RequestBody</code> binds incoming HTTP JSON body to DTO. <code>@PathVariable</code> extracts parameters directly from URL path (e.g. <code>{id}</code>).", style_body), Paragraph("Parameters in <code>ProductController</code>", style_body)],
    ]
    t_annos = Table(annos_data, colWidths=[120, 260, 143])
    t_annos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(1, len(annos_data)):
        if i % 2 == 1:
            t_annos.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_annos)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Controller vs Service vs Repository in this Project", style_h2))
    layers_explanation = (
        "<b>Interview Golden Rule: Separation of Concerns</b><br/>"
        "• <b>Controller (<code>ProductController</code>):</b> Handles HTTP layer only (URL matching, JSON parsing, HTTP status codes 200/400/404). <i>Never put business logic or DB calls here!</i><br/>"
        "• <b>Service (<code>ProductServiceImpl</code>):</b> Handles business logic (e.g., verifying product exists, setting default status to 'Manufactured', ensuring status update does not overwrite name/origin).<br/>"
        "• <b>Repository (<code>ProductRepository</code>):</b> Handles data persistence only (translating method calls into PostgreSQL SQL queries via Spring Data JPA)."
    )
    story.append(make_card(None, [layers_explanation], CARD_BG, BORDER_COLOR))

    # END OF PAGE 4
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TECHNICAL VIVA QUESTIONS (Side-by-Side 2-Column Layout to fit 1 page)
    # =========================================================================
    story.append(Paragraph("PAGE 5 - Technical Viva Questions from the Project", style_page_title))
    story.append(Paragraph("Top 20 high-frequency viva interview questions with crisp, verbal-ready answers.", style_page_subtitle))

    qas_col1 = [
        ("1. What is your project about?",
         "Centralized RESTful backend developed with Spring Boot and PostgreSQL to track product supply chain lifecycles from manufacturing to delivery."),
        ("2. What real-world problem does it solve?",
         "Eliminates manual logging discrepancies and delayed tracking in warehouses by providing real-time, milestone status updates for logistics."),
        ("3. Why did you select PostgreSQL instead of MySQL?",
         "PostgreSQL offers superior adherence to strict SQL standards, advanced concurrency control (MVCC), and high reliability for transactional tracking."),
        ("4. What are the main modules in your application?",
         "Controller module (HTTP routing), Service module (business rules), Repository module (data access), DTO module (input validation), and Config module (CORS)."),
        ("5. How does product tracking actually work?",
         "When created, status defaults to 'Manufactured'. As items move through logistics, warehouse operators hit PUT endpoint with product ID to advance status to 'Shipped' or 'Delivered'."),
        ("6. How is product data stored in the database?",
         "Inside PostgreSQL table <code>products</code> with columns: <code>id</code> (BIGINT PK), <code>name</code> (VARCHAR), <code>origin</code> (VARCHAR), and <code>status</code> (VARCHAR)."),
        ("7. How does the application connect to PostgreSQL?",
         "Via Spring Boot's HikariCP connection pool configured in <code>application.properties</code> using the PostgreSQL JDBC driver and standard DB credentials."),
        ("8. What happens when a product ID is not found?",
         "<code>findById(id)</code> returns <code>Optional.empty()</code>, throwing custom <code>ResourceNotFoundException</code>, returning a clean 404 response."),
        ("9. How do you protect product name during status update?",
         "In <code>ProductServiceImpl</code>, status update method fetches existing entity and executes <code>existingProduct.setStatus(dto.getStatus())</code>, leaving name/origin untouched."),
        ("10. How are product IDs generated?",
         "Via <code>@GeneratedValue(strategy = IDENTITY)</code>, which delegates auto-incrementing integer key generation to PostgreSQL's native <code>SERIAL</code> sequence."),
    ]

    qas_col2 = [
        ("11. What is Dependency Injection (DI)?",
         "A design pattern where an object receives its dependencies from an external container (Spring IoC) rather than instantiating them directly with <code>new</code>."),
        ("12. What is Inversion of Control (IoC)?",
         "The architectural principle where object creation, lifecycle, and wiring is inverted from the developer to the Spring framework container."),
        ("13. Why use Constructor Injection over @Autowired on fields?",
         "Constructor injection ensures dependencies are immutable (final), makes classes easily testable, and prevents uninitialized object instances."),
        ("14. What is an ORM?",
         "Object-Relational Mapping (ORM) maps Java classes to database tables and object instances to table rows, removing manual SQL query coding."),
        ("15. What is the difference between JPA and Hibernate?",
         "JPA is the standard Java specification/interface; Hibernate is the actual ORM library that implements JPA and converts operations into SQL queries."),
        ("16. What is a DTO and why not expose the Entity directly?",
         "DTOs (Data Transfer Objects) encapsulate incoming API data, preventing over-posting attacks, decoupling DB schema from API contracts, and adding validation."),
        ("17. What is the purpose of application.properties?",
         "Spring Boot's central configuration file used to specify server ports, database URLs, credentials, JPA behaviors, and logging levels without changing code."),
        ("18. What is the difference between HTTP POST and PUT?",
         "POST creates a new resource on the server (non-idempotent). PUT updates or replaces an existing resource identified by a specific URI (idempotent)."),
        ("19. What is the difference between HTTP GET and DELETE?",
         "GET retrieves data without modifying server state (safe/idempotent). DELETE removes the specified resource from the server (idempotent)."),
        ("20. What is CORS and why is CorsConfig.java necessary?",
         "Cross-Origin Resource Sharing is a browser security mechanism. <code>CorsConfig</code> allows frontend apps on other domains/ports to access port 5000 safely."),
    ]

    col1_elements = [Paragraph("<b>Part A: Project-Based Questions</b>", style_h2), Spacer(1, 2)]
    for q, a in qas_col1:
        col1_elements.append(Paragraph(f"<b>{q}</b>", style_qa_box))
        col1_elements.append(Paragraph(a, style_qa_box))
        col1_elements.append(Spacer(1, 2.5))

    col2_elements = [Paragraph("<b>Part B: Core Technical Questions</b>", style_h2), Spacer(1, 2)]
    for q, a in qas_col2:
        col2_elements.append(Paragraph(f"<b>{q}</b>", style_qa_box))
        col2_elements.append(Paragraph(a, style_qa_box))
        col2_elements.append(Spacer(1, 2.5))

    t_viva_2col = Table([[col1_elements, col2_elements]], colWidths=[256, 257])
    t_viva_2col.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 6),
        ('LEFTPADDING', (1,0), (1,-1), 6),
        ('RIGHTPADDING', (1,0), (1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_viva_2col)

    # END OF PAGE 5
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: CROSS-QUESTIONING & SCENARIO-BASED VIVA
    # =========================================================================
    story.append(Paragraph("PAGE 6 - Cross-Questioning & Scenario-Based Viva", style_page_title))
    story.append(Paragraph("Detailed answers for the tricky follow-up questions interviewers ask to test your practical depth.", style_page_subtitle))

    cross_questions = [
        ("1. Why did you migrate from Node.js/Express to Spring Boot?",
         "<b>Answer:</b> Node.js is lightweight, but Spring Boot provides enterprise-grade type safety, structured 3-tier architecture, built-in dependency injection, and Spring Data JPA. For enterprise supply chains requiring transactional integrity and team scalability, Spring Boot is far more robust.",
         "<i>Follow-up: Did you have to change your frontend?</i> No, because we preserved the exact same HTTP routes, request bodies, JSON response formats, and port 5000."),
        
        ("2. Why separate Controller, Service, and Repository instead of writing DB queries in Controller?",
         "<b>Answer:</b> Separation of Concerns. Controllers should only handle web/HTTP concerns. If business rules change (e.g. adding a new tracking status), we only modify the Service layer without touching the HTTP layer, ensuring maintainability and clean unit testing.",
         "<i>Follow-up: What principle is this?</i> The Single Responsibility Principle (SRP from SOLID)."),

        ("3. What happens behind the scenes when a user sends POST /products?",
         "<b>Answer:</b> 1. Request hits Tomcat on port 5000 -&gt; 2. <code>DispatcherServlet</code> routes to <code>ProductController.createProduct()</code> -&gt; 3. Jackson deserializes JSON into <code>ProductRequestDto</code> and validates <code>@NotBlank</code> -&gt; 4. Service applies business defaults -&gt; 5. Repository calls Hibernate -&gt; 6. Hibernate executes SQL INSERT via JDBC into PostgreSQL -&gt; 7. Generated ID is assigned and returned as JSON.",
         None),

        ("4. What happens if the PostgreSQL database goes down during application runtime?",
         "<b>Answer:</b> HikariCP connection pool attempts to reconnect. If unavailable, it throws a <code>CannotCreateTransactionException</code> or <code>JDBCConnectionException</code>. Our <code>GlobalExceptionHandler</code> catches it and returns a clean 500 Internal Server Error without exposing DB passwords or stack traces.",
         "<i>Follow-up: How to monitor DB health?</i> By adding Spring Boot Actuator with <code>/actuator/health</code>."),

        ("5. What happens if someone submits an invalid ID format like PUT /products/abc/status?",
         "<b>Answer:</b> Spring's DispatcherServlet fails to convert string 'abc' to <code>Long</code>. It triggers a <code>MethodArgumentTypeMismatchException</code>. Our centralized exception handler intercepts it and returns HTTP 400 Bad Request with a clear message: 'Invalid parameter: id must be of type Long'.",
         None),

        ("6. How would you prevent invalid backward status updates (e.g. Delivered -> Manufactured)?",
         "<b>Answer:</b> In <code>ProductServiceImpl</code>, implement a state transition validator: if current status is 'Delivered', reject updates to 'Manufactured' or 'Shipped' by throwing an <code>IllegalStateException</code> (HTTP 400).",
         None),

        ("7. How would you track the complete audit history (timestamp, location, user) of each status change?",
         "<b>Answer:</b> Create a secondary entity named <code>ProductHistory</code> with fields: <code>id</code>, <code>productId</code>, <code>previousStatus</code>, <code>newStatus</code>, <code>timestamp</code>, and <code>updatedBy</code>. Every time <code>updateProductStatus()</code> is called, insert a new record into <code>product_history</code> within the same <code>@Transactional</code> method.",
         None),

        ("8. How would you add user authentication to this system?",
         "<b>Answer:</b> Add <code>spring-boot-starter-security</code> with JWT (JSON Web Tokens). Create a <code>User</code> entity with roles (e.g. <code>ROLE_WAREHOUSE</code>, <code>ROLE_ADMIN</code>). Secure endpoints so only authenticated warehouse personnel can call POST, PUT, and DELETE.",
         None),

        ("9. How would you support hundreds of thousands of products without slowing down GET /products?",
         "<b>Answer:</b> Implement <b>Pagination and Sorting</b> using Spring Data's <code>Pageable</code>: <code>Page&lt;Product&gt; findAll(Pageable pageable)</code>. The client can request <code>GET /products?page=0&size=20</code>, preventing out-of-memory errors by fetching small batches.",
         None),

        ("10. How would you deploy this application in a production environment?",
         "<b>Answer:</b> Build the standalone executable JAR using <code>mvn clean package -DskipTests</code>, package it into a lightweight Docker container running OpenJDK 21, and deploy it to a cloud VM (AWS EC2 / Azure) pointing to an AWS RDS PostgreSQL instance.",
         None),
    ]

    for item in cross_questions:
        q = item[0]
        ans = item[1]
        fu = item[2] if len(item) > 2 else None
        
        content = [Paragraph(ans, style_body)]
        if fu:
            content.append(Paragraph(fu, style_callout))
        story.append(make_card(q, content, CARD_BG, BORDER_COLOR))
        story.append(Spacer(1, 3))

    # END OF PAGE 6
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: FINAL INTERVIEW REVISION SHEET
    # =========================================================================
    story.append(Paragraph("PAGE 7 - Final Interview Revision Sheet & Cheat Sheet", style_page_title))
    story.append(Paragraph("Fast-revision summary sheet to review 30 minutes before your placement interview.", style_page_subtitle))

    story.append(Paragraph("1. Rapid Project Fact Sheet", style_h2))

    facts_data = [
        [Paragraph("<b>Project Name:</b> Supply Chain Product Tracking System", style_body), Paragraph("<b>Target Port:</b> 5000 (<code>http://localhost:5000</code>)", style_body)],
        [Paragraph("<b>Language:</b> Java 21 (LTS)", style_body), Paragraph("<b>Build Tool:</b> Apache Maven (<code>pom.xml</code>)", style_body)],
        [Paragraph("<b>Framework:</b> Spring Boot 3.3.5 (Spring MVC)", style_body), Paragraph("<b>Database:</b> PostgreSQL 16 (Port 5432)", style_body)],
        [Paragraph("<b>ORM Engine:</b> Hibernate 6 (via Spring Data JPA)", style_body), Paragraph("<b>Connection Pool:</b> HikariCP (built-in default)", style_body)],
        [Paragraph("<b>Main DB Table:</b> <code>products</code> (id, name, origin, status)", style_body), Paragraph("<b>Key Lifecycle:</b> <code>Manufactured -&gt; Shipped -&gt; Delivered</code>", style_body)],
        [Paragraph("<b>Primary Endpoints:</b> GET /, GET /products, POST /products, PUT /products/{id}/status, DELETE /products/{id}", style_body), Paragraph("<b>Architecture:</b> 3-Tier Layered Architecture (Controller-Service-Repo)", style_body)],
    ]
    t_facts = Table(facts_data, colWidths=[261, 262])
    t_facts.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_facts)
    story.append(Spacer(1, 3.5))

    story.append(Paragraph("2. Technical Keywords in Plain English (1-Line Definitions)", style_h2))

    keywords_data = [
        ("REST API", "Stateless web architectural style exchanging raw data (JSON) via standard HTTP verbs (GET, POST, PUT, DELETE)."),
        ("Dependency Injection (DI)", "Passing required dependencies into a class rather than the class creating them directly with 'new'."),
        ("Inversion of Control (IoC)", "The framework manages object lifecycles and wiring instead of manual developer control."),
        ("JPA (Jakarta Persistence API)", "Standard Java specification interface for object-relational mapping."),
        ("Hibernate", "Popular ORM library implementing JPA specifications to translate Java objects into SQL queries."),
        ("Entity", "A Java class annotated with <code>@Entity</code> representing a relational database table row."),
        ("Repository", "A Spring Data interface (<code>JpaRepository</code>) providing out-of-the-box database CRUD operations."),
        ("DTO (Data Transfer Object)", "An object dedicated to carrying data across network boundaries without exposing database entities."),
        ("Controller", "Web-layer class annotated with <code>@RestController</code> that maps incoming HTTP requests to methods."),
        ("Service", "Class holding core business logic, validation rules, and transaction boundaries (<code>@Service</code>)."),
        ("JDBC Driver", "Database-specific communication adapter translating Java database calls into network socket protocols."),
        ("Maven", "Project management tool handling dependencies, compilation, and building executable JAR packages."),
    ]

    kw_cells = []
    for term, definition in keywords_data:
        kw_cells.append([
            Paragraph(f"<b>{term}</b>", style_body_bold),
            Paragraph(definition, style_body)
        ])
    t_kw = Table(kw_cells, colWidths=[130, 393])
    t_kw.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for i in range(len(kw_cells)):
        if i % 2 == 1:
            t_kw.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), BG_LIGHT)]))
    story.append(t_kw)
    story.append(Spacer(1, 3.5))

    story.append(Paragraph("3. Senior Placement Trainer's Interview Advice", style_h2))
    
    tips = (
        "• <b>How to start confidently:</b> Speak clearly. Begin with your 1-minute pitch. Frame the project around solving a logistics tracking problem.<br/>"
        "• <b>How to answer when you don't know:</b> Never guess blindly or say 'I don't know'. Instead say: <i>\"I haven't implemented that specific feature yet, but based on my understanding of Spring Boot, it would involve...\"</i><br/>"
        "• <b>Own your individual contribution:</b> State proudly that you wrote the Java controllers, services, JPA mappings, and tested all endpoints on port 5000.<br/>"
        "• <b>5 Mistakes to Avoid:</b> (1) Memorizing code lines instead of understanding request flow; (2) Confusing JPA with Hibernate; (3) Saying business logic is inside the Controller; (4) Claiming you used advanced microservices when this is a clean, solid monolith; (5) Talking too fast."
    )
    story.append(make_card("Trainer Pro-Tips for Service-Company Interviews", [tips], ACCENT_BG, colors.HexColor("#93C5FD")))
    story.append(Spacer(1, 3.5))

    # Pre-interview checklist
    checklist = (
        "<b>Pre-Interview Confidence Checklist:</b><br/>"
        "[ ✔ ] Can I explain the 1-minute project pitch fluently without hesitation?<br/>"
        "[ ✔ ] Can I trace a request step-by-step from <code>POST /products</code> down to the PostgreSQL INSERT?<br/>"
        "[ ✔ ] Do I know the difference between <code>@RestController</code>, <code>@Service</code>, and <code>@Repository</code>?<br/>"
        "[ ✔ ] Can I explain why we migrated from Node.js to Spring Boot for enterprise type safety and structure?"
    )
    story.append(make_card(None, [checklist], CARD_BG, BORDER_COLOR))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully Generated: {filename}")

if __name__ == "__main__":
    build_pdf()

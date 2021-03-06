# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Provide a 'Big Bank' example.

Illustrate how to create a software architecture diagram using code, based on
https://github.com/structurizr/dsl/blob/master/examples/big-bank-plc.dsl.
"""


import logging

from structurizr import Workspace
from structurizr.model import Enterprise, Location, Tags
from structurizr.view import ElementStyle, PaperSize, RelationshipStyle, Shape


def main():
    """Standard entry point for examples.  Do not rename."""
    return create_big_bank_workspace()


def create_big_bank_workspace():
    """Create the big bank example."""

    workspace = Workspace(
        name="SCP v1.0",
        description=(
            "Sistema de Contatacion de Personal v1.0 "
        ),
    )

    existing_system_tag = "Existing System"
    business_staff_tag = "Bank Staff"
    web_browser_tag = "Web Browser"
    mobile_app_tag = "Mobile App"
    database_tag = "Database"
    failover_tag = "Failover"
    bounded_context_tag = "Bounded Context"

    model = workspace.model
    views = workspace.views

    model.enterprise = Enterprise(name="Open Solutions -  Business & Technologies")

    # people and software systems
    postulante = model.add_person(
        location=Location.External,
        name="Postulante",
        description="Persona para que intenta alcanzar una puesto de tabajo y apertura una cuenta temporal.",
        id="postulante",
    )

    jefe_rrh = model.add_person(
        location=Location.Internal,
        name="Jefatura de recursos humanos",
        description="El decisor de generacion de puestos de trabajo y la inicializacion de una nueva convocatoria",
        id="jefeRrh",
    )
    jefe_rrh.tags.add(business_staff_tag)
    #postulante.interacts_with(
    #    jefe_rrh, "Asks questions to", technology="Telephone"
    #)

    comite_evaluador = model.add_person(
        location=Location.Internal,
        name="Comite Evaluador",
        description="Evalua a los postulantes de la convocatoria",
        id="comiteEvaluador",
    )
    comite_evaluador.tags.add(business_staff_tag)

    sistema_contratacion_personal = model.add_software_system(
        location=Location.Internal,
        name="Sistema de contratacion",
        description=(
            "Permite la publicacion de una convocatoria, registro de postulantes y evaluacion de los mismos"
        ),
        id="sistemaContratacionPersonal",
    )
    postulante.uses(
        sistema_contratacion_personal, "Se registra mediante una cuenta temporal. Rinde las evaluaciones"
    )
    jefe_rrh.uses(sistema_contratacion_personal, "Uses")
    comite_evaluador.uses(sistema_contratacion_personal, "Uses")
    
    mainframe_business_system = model.add_software_system(
        location=Location.Internal,
        name="Mainframe Business System",
        description=(
            "Sistema transacional de la empresa. Aca tambien se registra los postulantes aceptados como empleados "
        ),
        id="mainframe",
    )
    mainframe_business_system.tags.add(existing_system_tag)
    sistema_contratacion_personal.uses(
        mainframe_business_system,
        "Registra al nuevo personal",
    )
    
    email_system = model.add_software_system(
        location=Location.Internal,
        name="Sistema de correos",
        description="Sistema de correos con Squirrelmail",
        id="email",
    )
    email_system.tags.add(existing_system_tag)
    email_system.delivers(
        destination=postulante,
        description="Sends e-mails to",
    )
    sistema_contratacion_personal.uses(
        destination=email_system,
        description="Sends e-mail using",
    )
     
    portal = model.add_software_system(
        location=Location.Internal,
        name="Portal Institucional",
        description="Web Estatica con informacion de la Organizacion.",
        id="portal",
    )
    portal.tags.add(existing_system_tag)
    #portal.uses(mainframe_business_system, "Uses")
    postulante.uses(portal, "Busca oportunidades de trabajo")
    sistema_contratacion_personal.uses(portal, "Uses")
    
    # containers
    single_page_application = sistema_contratacion_personal.add_container(
        "Single-Page Application",
        "Provee la funcionalidad para los postulantes y los business workers.",
        "Flutter application",
        id="singlePageApplication",
    )
    single_page_application.tags.add(web_browser_tag)
    postulante.uses(single_page_application, "Uses", technology="JSON/HTTPS")
    jefe_rrh.uses(single_page_application, "Uses", technology="JSON/HTTPS")
    comite_evaluador.uses(single_page_application, "Uses", technology="JSON/HTTPS")

    mobile_app = sistema_contratacion_personal.add_container(
        "Mobile App",
        "Provee funcionalidad de avisos y comunicacion hacia los postulantes.",
        "Flutter mobile application",
        id="mobileApp",
    )
    mobile_app.tags.add(mobile_app_tag)
    postulante.uses(mobile_app, "Uses")

    
    api_application_container = sistema_contratacion_personal.add_container(
        "API Application",
        "Provee los EndPoints via a JSON/HTTPS API.",
        "NestJs - TypeScript",
        id="apiApplication",
    )
    api_application_container.uses(email_system, "Sends e-mail using", technology="SMTP")
    single_page_application.uses(api_application_container, "Makes API calls to" "JSON/HTTPS")
    mobile_app.uses(api_application_container, "Makes API calls to" "JSON/HTTPS")

    postulante_context_container = sistema_contratacion_personal.add_container(
        "Contexto Postulante",
        "Provee las funcionalidades para manejar el agregado Postulante",
        "Java and Spring MVC",
        id="postulanteContext",
    )
    postulante_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(postulante_context_container, "")

    convocatoria_context_container = sistema_contratacion_personal.add_container(
        "Contexto Convocatoria",
        "Provee las funcionalidades para manejar el agregado Convoocatoria",
        "Java and Spring MVC",
        id="convocatoriaContext",
    )
    convocatoria_context_container.tags.add(bounded_context_tag)
    api_application_container.uses(convocatoria_context_container, "")

    evaluaciones_context_container = sistema_contratacion_personal.add_container(
        "Contexto Evaliaciones",
        "Provee las funcionalidades para manejar el agregado Evaluaciones",
        "Java and Spring MVC",
        id="evaluacionesContext",
    )
    evaluaciones_context_container.tags.add(bounded_context_tag)
    evaluaciones_context_container.uses(
        mainframe_business_system,
        "Registra al nuevo personal",
    )
    api_application_container.uses(evaluaciones_context_container, "")

    database = sistema_contratacion_personal.add_container(
        "Database",
        "Stores user registration information, hashed authentication credentials, "
        "access logs, etc.",
        "Relational Database Schema",
        id="database",
    )
    database.tags.add(database_tag)
    postulante_context_container.uses(database, "Guarda los postulantes")
    convocatoria_context_container.uses(database , "Guarda las convocatorias")
    evaluaciones_context_container.uses(database, "Guarda las evaluaciones")


    
    
    #web_application.uses(
    #    single_page_application, "Delivers to the postulantes web browser"
    #)
    #api_application_container.uses(database, "Reads from and writes to", technology="JDBC")
    #api_application_container.uses(mainframe_business_system, "Uses", technology="XML/HTTPS")
    


    
    # COMPONENTS
    # - for a real-world software system, you would probably want to extract the
    #   components using static analysis/reflection rather than manually specifying
    #   them all

    # api_application_container - COMPONENTS
    signin_controller_component = api_application_container.add_component(
        name="Sign In Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="signinController",
    )
    single_page_application.uses(signin_controller_component, "Makes API calls to", "JSON/HTTPS")
    mobile_app.uses(signin_controller_component, "Makes API calls to", "JSON/HTTPS")

    reset_password_controller_component = api_application_container.add_component(
        name="Reset Password Controller",
        description="Allows users to reset their passwords with a single use URL.",
        technology="NestJs - TypeScript",
        id="resetPasswordController",
    )
    single_page_application.uses(reset_password_controller_component, "Makes API calls to", "JSON/HTTPS")
    mobile_app.uses(reset_password_controller_component, "Makes API calls to", "JSON/HTTPS")

    email_component = api_application_container.add_component(
        name="E-mail Component",
        description="Sends e-mails to users.",
        technology="NestJs - TypeScript",
        id="emailComponent",
    )
    email_component.uses(email_system, "Sends e-mail using", technology="SMTP")
    reset_password_controller_component.uses(email_component, "Uses")

    security_component = api_application_container.add_component(
        name="Security Component",
        description="Provides functionality related to signing in, changing passwords, etc.",
        technology="NestJs - TypeScript, GoogleAuth",
        id="securityComponent",
    )
    security_component.uses(database, "Reads from and writes to", "JDBC")
    signin_controller_component.uses(security_component, "Uses")
    reset_password_controller_component.uses(security_component, "Uses")
    
    #convocatoria_context_container - COMPONENTS
    convocatoria_controller_component = convocatoria_context_container.add_component(
        name="Convocatoria Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaControllerComponent",
    )
    api_application_container.uses(convocatoria_controller_component)
    
    convocatoria_service_component = convocatoria_context_container.add_component(
        name="Convocatoria Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaServiceComponent",
    )
    convocatoria_controller_component.uses(convocatoria_service_component)

    convocatoria_repository_component = convocatoria_context_container.add_component(
        name="Convocatoria Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaRepository",
    )
    convocatoria_repository_component.uses(database)
    convocatoria_service_component.uses(convocatoria_repository_component)

    convocatoria_query_component = convocatoria_context_container.add_component(
        name="Convocatoria Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="convocatoriaQuery",
    )
    convocatoria_query_component.uses(database)
    convocatoria_controller_component.uses(convocatoria_query_component)
    
    # postulante_context_container - COMPONENTS
    postulante_controller_component = postulante_context_container.add_component(
        name="Postulante Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="postulanteControllerComponent",
    )
    api_application_container.uses(postulante_controller_component)
    
    postulante_service_component = postulante_context_container.add_component(
        name="Postulante Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="postulanteServiceComponent",
    )
    postulante_controller_component.uses(postulante_service_component)

    postulante_repository_component = postulante_context_container.add_component(
        name="Postulante Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="postulanteRepository",
    )
    postulante_repository_component.uses(database)
    postulante_service_component.uses(postulante_repository_component)

    postulante_query_component = postulante_context_container.add_component(
        name="Postulante Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="postulanteQuery",
    )
    postulante_query_component.uses(database)
    postulante_controller_component.uses(postulante_query_component)

    # evaluaciones_context_container - COMPONENTS
    evaluaciones_controller_component = evaluaciones_context_container.add_component(
        name="Evaluaciones Controller",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesControllerComponent",
    )
    api_application_container.uses(evaluaciones_controller_component)
    
    evaluaciones_service_component = evaluaciones_context_container.add_component(
        name="Evaluaciones Application Service",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesServiceComponent",
    )
    evaluaciones_controller_component.uses(evaluaciones_service_component)

    evaluaciones_repository_component = evaluaciones_context_container.add_component(
        name="Evaluaciones Repository",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesRepository",
    )
    evaluaciones_repository_component.uses(database)
    evaluaciones_service_component.uses(evaluaciones_repository_component)

    evaluaciones_query_component = evaluaciones_context_container.add_component(
        name="Evaluaciones Query",
        description="Allows users to sign in to the Internet Banking System.",
        technology="NestJs - TypeScript",
        id="evaluacionesQuery",
    )
    evaluaciones_query_component.uses(database)
    evaluaciones_controller_component.uses(evaluaciones_query_component)

    """
    # TODO:!
    # model.AddImplicitRelationships()

    # deployment nodes and container instances
    developer_laptop = model.add_deployment_node(
        environment="Development",
        name="Developer Laptop",
        description="A developer laptop.",
        technology="Microsoft Windows 10 or Apple macOS",
    )
    apache_tomcat = developer_laptop.add_deployment_node(
        name="Docker - Web Server",
        description="A Docker container.",
        technology="Docker",
    ).add_deployment_node(
        name="Apache Tomcat",
        description="An open source Java EE web server.",
        technology="Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    )
    apache_tomcat.add_container(web_application)
    apache_tomcat.add_container(api_application_container)

    developer_laptop.add_deployment_node(
        "Docker - Database Server", "A Docker container.", "Docker"
    ).add_deployment_node(
        "Database Server", "A development database.", "Oracle 12c"
    ).add_container(
        database
    )

    developer_laptop.add_deployment_node(
        "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    ).add_container(single_page_application)

    postulante_mobile_device = model.add_deployment_node(
        "Customer's mobile device", "", "Apple iOS or Android", environment="Live"
    )
    postulante_mobile_device.add_container(mobile_app)

    postulante_computer = model.add_deployment_node(
        "Customer's computer",
        "",
        "Microsoft Windows or Apple macOS",
        environment="Live",
    )
    postulante_computer.add_deployment_node(
        "Web Browser", "", "Chrome, Firefox, Safari, or Edge"
    ).add_container(single_page_application)

    big_bank_data_center = model.add_deployment_node(
        "Big Bank plc", "", "Big Bank plc data center", environment="Live"
    )

    live_web_server = big_bank_data_center.add_deployment_node(
        "bigbank-web***",
        "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
        "Ubuntu 16.04 LTS",
        instances=4,
        properties={"Location": "London and Reading"},
    )
    live_web_server.add_deployment_node(
        "Apache Tomcat",
        "An open source Java EE web server.",
        "Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    ).add_container(web_application)

    live_api_server = big_bank_data_center.add_deployment_node(
        "bigbank-api***",
        "A web server residing in the web server farm, accessed via F5 BIG-IP LTMs.",
        "Ubuntu 16.04 LTS",
        instances=8,
        properties={"Location": "London and Reading"},
    )
    live_api_server.add_deployment_node(
        "Apache Tomcat",
        "An open source Java EE web server.",
        "Apache Tomcat 8.x",
        instances=1,
        properties={"Xmx": "512M", "Xms": "1024M", "Java Version": "8"},
    ).add_container(api_application_container)

    primary_database_server = big_bank_data_center.add_deployment_node(
        "bigbank-db01",
        "The primary database server.",
        "Ubuntu 16.04 LTS",
        instances=1,
        properties={"Location": "London"},
    ).add_deployment_node(
        "Oracle - Primary", "The primary, live database server.", "Oracle 12c"
    )
    primary_database_server.add_container(database)

    big_bank_db_02 = big_bank_data_center.add_deployment_node(
        "bigbank-db02",
        "The secondary database server.",
        "Ubuntu 16.04 LTS",
        instances=1,
        properties={"Location": "Reading"},
    )
    big_bank_db_02.tags.add(failover_tag)
    secondary_database_server = big_bank_db_02.add_deployment_node(
        "Oracle - Secondary",
        "A secondary, standby database server, used for failover purposes only.",
        "Oracle 12c",
    )
    secondary_database_server.tags.add(failover_tag)
    secondary_database = secondary_database_server.add_container(database)

    # model.Relationships.Where(r=>r.Destination.Equals(secondary_database)).ToList()
    #   .ForEach(r=>r.tags.add(failover_tag))
    data_replication_relationship = primary_database_server.uses(
        secondary_database_server, "Replicates data to"
    )
    secondary_database.tags.add(failover_tag)
    """
    # views/diagrams
    system_landscape_view = views.create_system_landscape_view(
        key="SystemLandscape",
        description="Vision global del nuevo Sistema de Contratacion de Personal",
    )
    system_landscape_view.add_all_elements()
    system_landscape_view.paper_size = PaperSize.A4_Landscape
    
    system_context_view = views.create_system_context_view(
        software_system=sistema_contratacion_personal,
        key="SystemContext",
        description="The system context diagram for the Internet Banking System.",
    )
    system_context_view.enterprise_boundary_visible = True
    #system_context_view.add_all_elements()
    system_context_view.add_nearest_neighbours(sistema_contratacion_personal)
    system_context_view.paper_size = PaperSize.A4_Landscape
    
    container_view = views.create_container_view(
        software_system=sistema_contratacion_personal,
        key="Containers",
        description="The container diagram for the Sistema de Contratacion de Personal.",
    )
    container_view.add(postulante)
    container_view.add(jefe_rrh)
    container_view.add(comite_evaluador)
    container_view.add_all_containers()
    container_view.add(mainframe_business_system)
    container_view.add(email_system)
    container_view.paper_size = PaperSize.A4_Landscape
    
    component_apiApplication_view = views.create_component_view(
        container=api_application_container,
        key="Components",
        description="The component diagram for the API Application.",
    )
    component_apiApplication_view.add(mobile_app)
    component_apiApplication_view.add(single_page_application)
    component_apiApplication_view.add(database)
    component_apiApplication_view.add_all_components()
    component_apiApplication_view.add(email_system)
    component_apiApplication_view.paper_size = PaperSize.A4_Landscape

    component_convocatoriaContext_view = views.create_component_view(
        container=convocatoria_context_container,
        key="Components1",
        description="Diagrama de componentes del Bounded Context de Convocatoria.",
    )
    component_convocatoriaContext_view.add(api_application_container)
    component_convocatoriaContext_view.add(database)
    component_convocatoriaContext_view.add_all_components()
    component_convocatoriaContext_view.paper_size = PaperSize.A4_Landscape

    component_postulanteContext_view = views.create_component_view(
        container=postulante_context_container,
        key="Components2",
        description="Diagrama de componentes del Bounded Context de Postulantes.",
    )
    component_postulanteContext_view.add(api_application_container)
    component_postulanteContext_view.add(database)
    component_postulanteContext_view.add_all_components()
    component_postulanteContext_view.paper_size = PaperSize.A4_Landscape

    component_evaluacionesContext_view = views.create_component_view(
        container=evaluaciones_context_container,
        key="Components3",
        description="Diagrama de componentes del Bounded Context de Evaluaciones.",
    )
    component_evaluacionesContext_view.add(api_application_container)
    component_evaluacionesContext_view.add(database)
    component_evaluacionesContext_view.add_all_components()
    component_evaluacionesContext_view.paper_size = PaperSize.A4_Landscape


    """
    # systemLandscapeView.AddAnimation(sistema_contratacion_personal, postulante,
    #   mainframe_business_system, emailSystem)
    # systemLandscapeView.AddAnimation(portal)
    # systemLandscapeView.AddAnimation(postulanteServiceStaff, comite_evaluador)

    # systemContextView.AddAnimation(sistema_contratacion_personal)
    # systemContextView.AddAnimation(postulante)
    # systemContextView.AddAnimation(mainframe_business_system)
    # systemContextView.AddAnimation(emailSystem)

    # containerView.AddAnimation(postulante, mainframe_business_system, emailSystem)
    # containerView.AddAnimation(webApplication)
    # containerView.AddAnimation(singlePageApplication)
    # containerView.AddAnimation(mobile_app)
    # containerView.AddAnimation(apiApplication)
    # containerView.AddAnimation(database)

    # componentView.AddAnimation(singlePageApplication, mobile_app)
    # componentView.AddAnimation(signinController, securityComponent, database)
    # componentView.AddAnimation(accountsSummaryController,
    #   mainframe_business_systemFacade, mainframe_business_system)
    # componentView.AddAnimation(resetPasswordController, emailComponent, database)

    dynamic_view = views.create_dynamic_view(
        element=api_application_container,
        key="SignIn",
        description="Summarises how the sign in feature works in the single-page application.",
    )
    dynamic_view.add(
        single_page_application, signin_controller_component, "Submits credentials to"
    )
    dynamic_view.add(
        signin_controller_component, security_component, "Calls isAuthenticated() on"
    )
    dynamic_view.add(
        security_component, database, "select * from users where username = ?"
    )
    dynamic_view.paper_size = PaperSize.A5_Landscape

    development_deployment_view = views.create_deployment_view(
        software_system=sistema_contratacion_personal,
        key="DevelopmentDeployment",
        description="An example development deployment scenario for the Internet "
        "Banking System.",
        environment="Development",
    )
    development_deployment_view.add(developer_laptop)
    development_deployment_view.paper_size = PaperSize.A5_Landscape

    live_deployment_view = views.create_deployment_view(
        software_system=sistema_contratacion_personal,
        key="LiveDeployment",
        description="An example live deployment scenario for the Internet Banking "
        "System.",
        environment="Live",
    )
    live_deployment_view += big_bank_data_center
    live_deployment_view += postulante_mobile_device
    live_deployment_view += postulante_computer
    live_deployment_view += data_replication_relationship
    live_deployment_view.paper_size = PaperSize.A5_Landscape
    """
    # colours, shapes and other diagram styling
    styles = views.configuration.styles
    styles.add(ElementStyle(tag=Tags.SOFTWARE_SYSTEM, background="#1168bd", color="#ffffff"))
    styles.add(ElementStyle(tag=Tags.CONTAINER, background="#438dd5", color="#ffffff"))
    styles.add(ElementStyle(tag=Tags.COMPONENT, background="#85bbf0", color="#000000"))
    styles.add(ElementStyle(tag=Tags.PERSON, background="#08427b", color="#ffffff", shape=Shape.Person, font_size=22,))
    styles.add(ElementStyle(tag=existing_system_tag, background="#999999", color="#ffffff"))
    styles.add(ElementStyle(tag=business_staff_tag, background="#999999", color="#ffffff"))
    styles.add(ElementStyle(tag=web_browser_tag, shape=Shape.WebBrowser))
    styles.add(ElementStyle(tag=mobile_app_tag, shape=Shape.MobileDeviceLandscape))
    styles.add(ElementStyle(tag=database_tag, shape=Shape.Cylinder))
    styles.add(ElementStyle(tag=failover_tag, opacity=25))
    styles.add(ElementStyle(tag=bounded_context_tag, shape=Shape.Hexagon,background="#facc2e"))
    styles.add(RelationshipStyle(tag=failover_tag, opacity=25, position=70))
    
    

    return workspace

from structurizr import StructurizrClient, StructurizrClientSettings

if __name__ == "__main__":
    #logging.basicConfig(level="INFO")
    workspace = main()
    settings = StructurizrClientSettings(
        workspace_id=70821,
        api_key='53a88814-3283-4774-ada2-80b4ec1fcfc9',
        api_secret='55e7266e-1dc3-4117-a494-f856bdd072e3',
    )
    client = StructurizrClient(settings=settings)
    
    workspace.id = client.get_workspace().id
    client.put_workspace(workspace)

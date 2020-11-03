
function show_message(message){ // Mostrar alert de proceso realizado exitosamente 
    document.getElementById('message').innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
};

$(document).ready(() => {
    // variables
    let client_id, create_update, row, clients_view = 'Activo', count_click_ip = 1, order_ip='asc';

    // Llenar tabla de clientes
    function client_table () {
        $.ajax({
            url: 'consult_client', 
            method: 'POST', // usamos el metodo POST
            data:{
                clients_view: clients_view,
                order_ip: order_ip},
            success: (response) => {
                let template = '';
                let count = 1;
                response.forEach(record => {                
                    template += `
                        <tr>
                            <td class="column0">${record.id}</td>
                            <td>
                                <div class='text-center'>
                                    ${ count }
                                </div>
                            </td>
                            <td class="edit-status">${record.name}</td>
                            <td>${record.ip_adress}</td>
                            <td>
                                <div class='text-center'>
                                <div class='btn-group'>
                                <button class='btn btn-success btn-sm edit-client'>Editar</button>
                                <button class='btn btn-danger btn-sm delete-client'>Eliminar</button>
                                </div>
                                </div>
                            </td>
                        </tr>
                    `
                    count+=1;
                }); $('#client_table').html(template);
            }
        });
    } client_table();  

    // ver tabla de acuerdo al tipo de clientes seleccionado
    $('#view_select').on('change',() => {
        let vs = $('#view_select').val();
        if (vs == 'Ver activos'){clients_view = 'Activo'}
        else if (vs == 'Ver todos'){clients_view = 'all'}
        else if (vs == 'Ver inactivos'){clients_view = 'Inactivo'}
        client_table();
    });

    // Cambiar el orden de la tabla de clientes por el campo "ip"
    $(document).on('click','#order_ip', function() {
        count_click_ip += 1;

        if (count_click_ip % 2 == 0){
            order_ip = 'desc';
            client_table();
        }else{
            order_ip = 'asc';
            client_table();
        }
    })

    // Abrir un modal para editar el estado del cliente
    $(document).on('click','.edit-status', function() {
        row = $(this).closest("tr");
        client_id = parseInt(row.find('td:eq(0)').text());
        name = row.find('td:eq(2)').text();
        $("#status_form").trigger("reset");
        $(".modal-header").css( "background-color", "#D42929");
        $(".modal-header").css( "color", "white" );
        $(".modal-title").text(name);
        $('#client_status_modal').modal('show');

        $.ajax({
            url: 'upload_client',
            method: 'POST',
            data: { id: client_id },
            success: (response) => {
                $("#status").val(response.status);
            }            
        })     
    });

    // Enviar actualizacion de estado al servidor
    $('#status_form').submit((e) => {         
        e.preventDefault();
        status = $('#status').val(); 
        status_date = $('#status_date').val(); 
        
        $.ajax({
            url: 'update_status',
            method: 'POST',
            data : {
                id: client_id,
                status: status,
                status_date : status_date,
            },   
            success: () => {
                $('#client_status_modal').modal('hide');
                show_message('Estado actualizado correctamente');
                client_table();	
            }
        });
    });  

    //Buscar cliente
    $('#search').keyup(() => {
        let search = $('#search').val();
        $.ajax({
            url: 'search_client',
            method: 'POST',
            data: {
                clients_view: clients_view,
                name: search
            },
            success: (response) => {
                let template = '';
                let count = 1;
                response.forEach(record => {                    
                    template += `
                        <tr>
                            <td class="column0">${record.id}</td>
                            <td>
                                <div class='text-center'>
                                    ${ count }
                                </div>
                            </td>
                            <td class="edit-status">${record.name}</td>
                            <td>${record.ip_adress}</td>
                            <td>
                                <div class='text-center'>
                                <div class='btn-group'>
                                <button class='btn btn-success btn-sm edit-client'>Editar</button>
                                <button class='btn btn-danger btn-sm delete-client'>Eliminar</button>
                                </div>
                                </div>
                            </td>
                        </tr>
                    `
                    count+=1;
                });
                if (count==1){
                    template = `
                        <tr>
                            <td class="column0">0</td>
                            <td><div class='text-center'>0</div></td>
                            <td>Sin registro</td>
                            <td>Sin registro</td>
                            <td>Sin acciones</td>
                        </tr>
                    `
                }$('#client_table').html(template);
            }
        })
    })

    //Nuevo cliente
    $(".new-client").click(function(){
        create_update = 'add_client';        
        client_id = null;
        $("#client_form").trigger("reset");
        $(".modal-header").css( "background-color", "#D42929");
        $(".modal-header").css( "color", "white" );
        $(".modal-title").text("Nuevo cliente");
        $('#client_modal').modal('show');	    
    });

    // Editar cliente
    $(document).on("click", ".edit-client", function(){		        
        create_update = 'update_client';//editar
        row = $(this).closest("tr");	        
        client_id = parseInt(row.find('td:eq(0)').text()); //capturo el ID
        $.ajax({
            url: 'upload_client',
            method: 'POST',
            data: {id: client_id},
            success: (response) => {
                $("#name").val(response.name);
                $("#ip_adress").val(response.ip_adress);
                $("#home_adress").val(response.home_adress);
                $("#phone").val(response.phone);
                $("#month_payment").val(response.month_payment);
                $("#mbps").val(response.mbps);
                $("#install_date").val(response.install_date);           
            }            
        })   		            
        $(".modal-header").css("background-color", "#D42929");
        $(".modal-header").css("color", "white" );
        $(".modal-title").text("Editar Cliente");		
        $('#client_modal').modal('show');		   
    });

    // Enviar datos del formulario de clientes al servidor
    $('#client_form').submit(function(e){                         
        e.preventDefault();
        name = $.trim($('#name').val());    
        ip_adress = $.trim($('#ip_adress').val());
        home_adress = $.trim($('#home_adress').val());    
        phone = $.trim($('#phone').val());    
        month_payment = $.trim($('#month_payment').val());
        mbps = $.trim($('#mbps').val());
        install_date = $.trim($('#install_date').val());                         
            $.ajax({
                url: create_update,
                method: "POST",  
                data:  {id:client_id,name:name,ip_adress:ip_adress,
                    home_adress:home_adress, phone:phone, month_payment:month_payment,
                    mbps:mbps, install_date: install_date},    
                success: () => {
                    client_table();
                }
            });			        
        $('#client_modal').modal('hide');
        if (create_update=='add_client'){
            show_message('Cliente registrado satisfactoriamente');
        } else {
            show_message('Los datos del cliente han sido actualizados satisfactoriamente');
        }
    });

    // Eliminar cliente
    $(document).on("click", ".delete-client", function(){
        row = $(this).closest("tr");           
        name = row.find('td:eq(2)').text();	
        let request = confirm("¿Está seguro de eliminar el cliente "+name+"?");                
        if (request) {            
            $.ajax({
                url: "delete_client",
                method: "POST",  
                data:  {id: client_id},    
                success: function() {
                    client_table();
                    show_message('Cliente eliminado satisfactoriamente');                  
                }
            });	
        }
    });

});
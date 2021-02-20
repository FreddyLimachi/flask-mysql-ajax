
function show_message(message){ // Mostrar alert de proceso realizado exitosamente 
    document.getElementById('message').innerHTML = `
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>`
};

function empty_history(){ // Indicar que no existen registros en la tabla de historial
    template = `
        <tr>
            <td class="column0">0</td>
            <td><div class='text-center'>0</div></td>
            <td>Sin registro</td>
            <td>Sin registro</td>
            <td>Sin registro</td>
            <td>Sin acciones</td>
        </tr>
    `
    $('#history_table').html(template);
}; empty_history();

$(document).ready(() => {
    // variables
    let client_id, history_id, row, clients_view = 'All', order_ip = 'asc';
    // Arreglo de meses
    let months_array = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];


    // Capturar cambio en el select de clientes
    $('#client_select').on('change',()=> {
        history_table();
        if ($('#client_select').val()!='Elige un cliente'){
            client_id = $('#client_select').val();
            $.ajax({
                url: 'upload_client',
                method: 'POST',
                data: {id: client_id},
                success: (response) => {
                    $('#payment').val(response.month_payment);             
                }            
            })      
        } else {
            $('#payment').val('');
        }
    });


    // Rellenar el select de clientes
    function client_select () {
        $.ajax({
            url:   'consult_client',
            method:  'POST',
            data: {clients_view: clients_view,
                order_ip: order_ip
        },
            success:  function (response) {
                $('#client_select').find('option').remove();
                $('#client_select').append('<option value="0">Elige un cliente</option>');
                response.forEach(record => {
                    $('#client_select').append('<option value="' + record.id + '">' + record.name + '</option>');
                })
            }
        });
    }; client_select ();


    // Rellenar la tabla historial de acuerdo al cliente establecido por el usuario
    function history_table () {
        let client_id = $('#client_select').val();
        $.ajax({
            url: 'consult_history', 
            method: 'POST', //usamos el metodo POST
            data:{id: client_id},
            success: (response) => {
                let template = '';
                let count = 1;
                response.forEach(record => {
                    template += `
                        <tr>
                            <td class="column0">${record.history_id}</td>
                            <td>
                                <div class='text-center'>
                                    ${ count }
                                </div>
                            </td>
                            <td>${record.description}</td>
                            <td>${record.payment_date}</td>
                            <td>${record.payment}</td>
                            <td>
                                <div class='text-center'>
                                <div class='btn-group'>
                                <button class='btn btn-success btn-sm edit-history'>Editar</button>
                                <button class='btn btn-danger btn-sm delete-history'>Eliminar</button>
                                </div>
                                </div>
                            </td>
                        </tr>
                    `
                    count+=1;
                });
                $('#history_table').html(template);
            }
        });
    }


    // Editar registro del historial
    $(document).on("click", ".edit-history", function () {	        
        row = $(this).closest("tr");	        
        history_id = parseInt(row.find('td:eq(0)').text()); //capturo el ID		      
        description = row.find('td:eq(2)').text();
        date_edit = row.find('td:eq(3)').text();
        payment_edit = row.find('td:eq(4)').text();
        
        $("#description").val(description);
        $("#date_edit").val(date_edit);
        $("#payment_edit").val(payment_edit);
        $(".modal-header").css("background-color", "#D42929");
        $(".modal-header").css("color", "white" );
        $(".modal-title").text("Editar historial");		
        $('#history_modal').modal('show');		   
    });


    // Eliminar registro del historial
    $(document).on("click", ".delete-history", function()  {
        row = $(this);           
        history_id = parseInt($(this).closest('tr').find('td:eq(0)').text());		    
        let request = confirm("¿Está seguro de eliminar este registro?");                
        if (request) {            
            $.ajax({
              url: "delete_history",
              method: "POST", 
              data:  {history_id:history_id},    
              success: () => {
                  history_table();
                  show_message('Registro eliminado satisfactoriamente');                  
               }
            });	
        }
    });


    // Enviar datos del formulario del historial al servidor
    $('#history_form').submit((e) => {         
        e.preventDefault();
        description = $.trim($('#description').val());    
        payment_date = $.trim($('#date_edit').val());
        payment = $.trim($('#payment_edit').val());    
            $.ajax({
                url: 'update_history',
                method: 'POST',
                data : {
                    history_id: history_id,
                    description: description,
                    payment_date: payment_date,
                    payment : payment
                },   
                success: () => {
                    history_table();
                }
            });			        
        $('#history_modal').modal('hide');
        show_message('Registro actualizado satisfactoriamente');	
    });


    // Registrar registro en el historial
    $('#payment_form').submit((e) => {                         
        e.preventDefault();
        client_id = $.trim($('#client_select').val());    
        year_month = $.trim($('#year_month').val());
        payment = $.trim($('#payment').val());    
        payment_date = $.trim($('#payment_date').val());
        
        m=year_month.slice(5, 7);
        month=months_array[m-1];
        year = year_month.slice(0, 4);
        description = 'Pago '+month+' '+year;

        year = payment_date.slice(0, 4);
        month = payment_date.slice(5, 7);
        day = payment_date.slice(8, 10);
        
        payment_date = day+'/'+month+'/'+year;
        
            $.ajax({
            url: 'add_history',
            method: 'POST',
            data : {
                id : client_id,
				description : description,
                payment : payment,
                payment_date : payment_date
			},   
            success: () => {
                history_table();
                show_message('Pago registrado satisfactoriamente');
            }
        });		        										     			
    });
});
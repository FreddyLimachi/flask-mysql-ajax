$(() => {
    
    //AJAX-CRUD EN LA PAGINA PRINCIPAL

    client_table = $('#client_table').DataTable({  
        "languaje":{
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
        },

        "ajax":{            
            url: "consult_client", 
            method: 'POST',
            dataSrc: "",
        },
        "columns":[
            {"data": "client_id"},
            {"data": "name"},
            {"data": "ip_adress"},
            {"data": "status"},
            {"defaultContent": `
                <div class='text-center'>
                    <div class='btn-group'>
                        <button class='btn btn-success btn-sm btn-edit'>Editar</button>
                        <button class='btn btn-danger btn-sm btn-delete'>Eliminar</button>
                    </div>
                </div>
            `}
        ]
    });
    
    $("#btnNuevo").click(() => {       
        url = '/add_client';
        client_id = '0'
        $("#client_form").trigger("reset");
        $(".modal-header").css( "background-color", "green");
        $(".modal-header").css( "color", "white" );
        $(".modal-title").text("Nuevo cliente");
        $('#modalCRUD').modal('show');	    
    });

    $(document).on("click", ".btn-edit", function () {
        url = '/edit_client';		        
        fila = $(this).closest("tr");	        
        client_id = parseInt(fila.find('td:eq(0)').text());        

        $("#name").val(name);
        $(".modal-header").css("background-color", "#007bff");
        $(".modal-header").css("color", "white" );
        $(".modal-title").text("Editar Usuario");		
        $('#modalCRUD').modal('show');		   
    });


    $('#client_form').submit((e) => {                         
        e.preventDefault();
        name = $.trim($('#name').val());    
        ip_adress = $.trim($('#ip_adress').val());
        direc = $.trim($('#direc').val());    
        phone = $.trim($('#phone').val());
        amount = $.trim($('#amount').val());    
        megas = $.trim($('#megas').val());
        date = $.trim($('#date').val());      
                              
            $.ajax({
            url: url,
            type: 'POST',  
            data : {
                client_id: client_id,
				name : name,
                ip_adress : ip_adress,
                direc : direc,
                phone : phone,
                megas : megas,
                amount : amount,
                date : date
			},   
            success: (data) => {
                client_table.ajax.reload(null, false);
            }
            });			        
        $('#modalCRUD').modal('hide');											     			
    });

    $(document).on("click", ".btn-delete", function() {
        fila = $(this);
        client_id = parseInt($(this).closest('tr').find('td:eq(0)').text());		    
        var respuesta = confirm("¿Está seguro de borrar el registro "+client_id+"?");                
        if (respuesta) {            
            $.ajax({
                url: "delete_client",
                type: "POST",
                datatype:"json",    
                data:  {client_id:client_id},    
                success: () => {
                    client_table.row(fila.parents('tr')).remove().draw();                  
                }
            });	
        }
    });

    //AJAX-CRUD EN LA PAGINA DE HISTORIALES

    $('#history_form').submit((e) => {                         
        e.preventDefault();
        description = $.trim($('#description').val());    
        date_edit = $.trim($('#date_edit').val());
        payment_edit = $.trim($('#payment_edit').val());           
            $.ajax({
            url: url,
            type: 'POST',  
            data : {
                history_id: history_id,
                description: description,
				date_edit : date_edit,
                payment_edit : payment_edit,
			},   
            success: (data) => {
                history_table();
            }
            });			        
        $('#modalHistory').modal('hide');											     			
    });

    function history_table () {
        let name = $('#client_select').val();
        $.ajax({            
            url: "/consult_history", 
            method: 'POST',
            data: {name: name},
            success: (response) => {
                let records = response;
                let template = '';
                let count = 1;
                records.forEach(record => {
                    template += `
                        <tr>
                            <td style="visibility: hidden;">${record.history_id}</td>
                            <td>
                                <div class='text-center'>
                                    ${ count }
                                </div>
                            </td>
                            <td>${record.description}</>
                            <td>${record.date}</td>
                            <td>${record.payment}</td>
                            <td>
                                <div class='text-center'>
                                <div class='btn-group'>
                                <button class='btn btn-success btn-sm btn-edit-history'>Editar</button>
                                <button class='btn btn-danger btn-sm btn-delete-history'>Eliminar</button>
                                </div>
                                </div>
                            </td>
                        </tr>
                    `
                    count+=1;
                });
                $('#history_table').html(template)
            }
        });
    }

    $('#client_select').on('change',()=> {
        history_table();
    });    

    $('#payment_form').submit((e) => {                         
        e.preventDefault();
        name = $.trim($('#client_select').val());    
        year_month = $.trim($('#year_month').val());
        payment = $.trim($('#payment').val());    
        payment_date = $.trim($('#payment_date').val());                            
            $.ajax({
            url: 'add_history',
            type: 'POST',  
            data : {
                name : name,
				year_month : year_month,
                payment : payment,
                payment_date : payment_date,
			},   
            success: (data) => {
                history_table();
            }
            });		        										     			
    });

    $(document).on("click", ".btn-edit-history", function () {
        url = '/edit_history';		        
        fila = $(this).closest("tr");	        
        history_id = parseInt(fila.find('td:eq(0)').text()); //capturo el ID		         
        description = fila.find('td:eq(2)').text();
        date_edit = fila.find('td:eq(3)').text();
        payment_edit = fila.find('td:eq(4)').text();
        
        $("#description").val(description);
        $("#date_edit").val(date_edit);
        $("#payment_edit").val(payment_edit);
        $(".modal-header").css("background-color", "#007bff");
        $(".modal-header").css("color", "white" );
        $(".modal-title").text("Editar Historial");		
        $('#modalHistory').modal('show');		   
    });

    $(document).on("click", ".btn-delete-history", function()  {
        fila = $(this);           
        history_id = parseInt($(this).closest('tr').find('td:eq(0)').text()) ;		    
        var respuesta = confirm("¿Está seguro de borrar el registro "+history_id+"?");                
        if (respuesta) {            
            $.ajax({
              url: "delete_history",
              method: "POST",
              datatype:"json",    
              data:  {history_id:history_id},    
              success: () => {
                  history_table();                  
               }
            });	
        }
    });

});



$(function(){
    var cred = $('#comp_cred').val();
    cred = parseInt(cred);
    $(':input:radio[name=rating]:checked').val();
    $('input:radio[name=rating]:input[value=' + cred + ']').attr("checked", true);
    // 삭제
    var selectdata = new Object();
    $('.deleteBtn').on('click', function(e){
        var str = e.target.parentElement.id.split('_');
        selectdata.id = str[1];
        Swal.fire({
          icon: 'error',
          title: '삭제하시겠습니까?',
          showCancelButton: true,
          text: ''
        }).then(function(){
            $.ajax({
                url: "/textile/company/delete/", /* "{% url 'company:delete' %}", */
                data : JSON.stringify(selectdata),
                type:'json',
                contentType: 'application/json',
                method: "POST",
                success: function(data){
                    location.reload();
                },
                error: function(error){
                    console.log(error)
                }
            });
        });
        return false;
    });

    $('.editContBtn').on('click', function(){
        $('#editModal').modal('show');
        /* Modal 내부 input 내용 */
        var comp_name = $(this).parents().siblings('.compName')[0].innerText;
        var facility_name = $(this).parents().siblings('.facNum')[0].innerText;
        var facility_id = $(this).parents().siblings('.facilityId')[0].innerText;

        $('#compName').val(comp_name);
        $('#facNum').val(facility_name);
        $('#facility_id').val(facility_id);
        /* Modal 내부 input 내용 */

        /* edit */
        $('#editBtn').on('click', function(){
            var obj = new Object();
            obj.facility_name = $('#facNum').val();
            obj.facility_id = $('#facility_id').val();

            var url = "/textile/company/facility/list/edit/"; /* "{% url 'company:company.fac_list_edit'%}"; */
            $.ajax({
                url: url,
                method:'POST',
                contentType: false,
                processData: false,
                dataType :   "json",
                contentType :   "application/x-www-form-urlencoded; charset=UTF-8",
                data: JSON.stringify(obj),
                success: function(result){
                    location.reload();
                }
            });
        });
        /* edit */
    });

});
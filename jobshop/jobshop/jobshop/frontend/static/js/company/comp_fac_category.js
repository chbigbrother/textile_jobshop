// 카테고리 추가
$('.modal-upload-btn').on('click', function(){
    $('#uploadModal').modal('show');
});

$('#modal-upload').on('click', function(){
    var obj = new Object();
    obj.cat_id = '';
    obj.cat_name = $('#cat_name').val();
    obj.user_info = $('.user-info').eq(0).val();
    $.ajax({
        url: '/textile/company/facility/category/edit/',
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

// 수정
$('.edit_modal_show').on('click', function(){
    $('#editModal').modal("show");
    var cat_name = $(this).parents().siblings('.cat_name_val')[0].innerText;
    var cat_id = $(this).parents().prevObject[0].id.substr(5);

    $('#catname').val(cat_name);
    /* edit */
    $('#editBtn').on('click', function(){
        var obj = new Object();
        obj.cat_name = $('#catname').val();
        obj.cat_id = cat_id;
        obj.user_info = $('.user-info').eq(0).val();
        var url = '/textile/company/facility/category/edit/';
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
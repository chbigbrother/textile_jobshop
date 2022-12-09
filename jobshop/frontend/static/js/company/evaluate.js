$('.rateComp').on('click', function(){
    $('#rateModal').modal('show');
    $('#submitBtn').on('click', function(){
        $(':input:radio[name=rating]:checked').val();
    });
});
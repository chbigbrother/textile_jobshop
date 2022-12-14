function dateformat(value){
    var year = value.substring(0,4);
    var month = value.substring(4,6);
    var day = value.substring(6,8);
    var date = year + '-' + month + '-' + day;
    return date;
}
var customer_img = ['<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus-2.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus-2.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-phatplus.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus-2.png"/>',
'<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-customer-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>'
];
$(function(){
    const today = moment();
    function progress(from, to){
        var progress_init = to - from;
        var progress_now = to - today.format('YYYYMMDD');
        if (progress_now == 0) {
            var process_percent = '100';
        } else{
            var process_percent = parseInt(((progress_init - progress_now) / progress_init)*100).toString();
        }
        if (process_percent==0) { var badge = 'badge badge-pill badge-warning'; var label='?????? ?????? ???';}
        if (process_percent<100) { var badge = 'badge badge-pill badge-secondary'; var label='?????? ???';}
        if (process_percent==100) { var badge = 'badge badge-pill badge-success'; var label='?????? ??????';}
        return [process_percent, badge, label];
    }
    var grp_name = $("#group_name").val();
    // ?????? ?????? init
    flatpickr("#dateTo", {
           locale: Flatpickr.l10ns.ko,
           enableTime: false,
           dateFormat: "Y-m-d",
           disableMobile: true,
           defaultDate: $('#dateTo').val()
           // defaultDate: [today.format('YYYY-MM-DD')]
    });
    flatpickr("#dateFrom", {
           locale: Flatpickr.l10ns.ko,
           enableTime: false,
           dateFormat: "Y-m-d",
           disableMobile: true,
           defaultDate: $('#dateFrom').val()
    });
    function doSearch(dateFrom, dateTo){
        var obj = new Object();
        obj.dateFrom = $('#dateFrom').val().replace(/\-/g,'');
        obj.dateTo = $('#dateTo').val().replace(/\-/g,'');
        obj.groupName = $('#group_name').val();
        obj.groupId = $('#group_id').val();
        obj.userName = $('#user_name').val();
        obj.userId = $('#user_id').val();
        $.ajax({
            url: "/textile/order/fixed/schedule/", // "{% url 'order:fixed' %}",
            method:'GET',
            processData: false,
            type:'json',
            contentType: 'application/json',
            data: JSON.stringify(obj),
            success: function(data){
                /* **********************
                 ** data ??????
                 ** [[{'comp_name': '(???)??????', 'order_id': 'ORD006', 'amount': 3800, 'cust_name': '?????????',
                 **    'sch_date': '20220203', 'exp_date': '20220521', 'textile_name': '6KOS-FM'}], ['(???)??????']]
                 ********************** */
                console.log(data);
                var innerHTML = '';
                var inner = document.createElement('div');
                var div = document.createElement('div');
                div.className = 'multiple-items';
                var name = '';
                if(data['message'] == 'null'){
                    $('.data-row').html('<div class="col-lg-6">'+
                                                '<div class="card mb-4 py-3 border-left-primary" style="width:100%;">'+
                                                    '<div class="card-body">'+
                                                        '?????? ?????? ?????? ?????? ???????????? ???????????? ????????????. <br/> ???????????? / ???????????? ?????? ???????????? ?????? ??????????????? ???????????????.'+
                                                    '</div>'+
                                                '</div>');
                } else {
                    for(var i=0; i<data.length;i++){
                        var content_data = data[i];
                        var process = progress(content_data.work_str_date,content_data.work_end_date);
                        var process_percent = process[0];
                        var badge = process[1];
                        var label = process[2];
                        var process_percent = process[0];
                            var badge = process[1];
                            var label = process[2];
                            innerHTML += '<div class="col-xl-3">' +
                                '<div class="row">' +
                                    '<div class="col-xl-12">' +
                                        '<div class="card">' +
                                            '<div class="card-body">' +
                                                '<div class="row ">' +
                                                    '<div class="">' +
                                                        '<div class="update-profile d-flex">' +
                                                            customer_img[i] + // '<img src="https://img.icons8.com/external-phatplus-lineal-color-phatplus/64/000000/external-user-marketing-and-seo-phatplus-lineal-color-phatplus.png"/>' +

                                                        '</div>' +
                                                        '<div>' +
                                                            '<h3 class="fs-24 font-w600 mb-0">????????? : ' + content_data.cust_name + '</h3>' +
                                                            '<span class="text-primary d-block mb-4">???????????? : ' + dateformat(content_data.exp_date) + '</span>' +
                                                            '<span>???????????? : ' + content_data.order_id + '</span>' +
                                                            '<span class="text-primary d-block mb-4">?????? : ' + content_data.amount + 'yd</span>' +
                                                        '</div>' +

                                                    '</div>';
                                                    /* *******  company lists  ******* */
                                                    var data_arr = content_data.comp_name;
                                                    if (Array.isArray(data_arr)){
                                                        for(var k=0; k<data_arr.length;k++){
                                                            var comp_name = data[data.length-1][k]
                                                            innerHTML += '<div class="col-xl-4 col-xxl-7 col-sm-7 comp-content">' +
                                                            '<div class="loadmore-content">' +
                                                                '<div class="row" id="FeaturedCompaniesContent">' +
                                                                    '<div class="col-xl-12 col-sm-6 mt-4">' +
                                                                        '<div class="d-flex">' +
                                                                            '<span>' +
                                                                                '<img src="https://img.icons8.com/external-flat-icons-pack-pongsakorn-tan/64/000000/external-company-labor-day-flat-icons-pack-pongsakorn-tan.png"/>' +
                                                                            '</span>' +
                                                                            '<div class="featured">'+
                                                                                '<h4 class="fs-5 mb-1">' + content_data.comp_name + '</h4>'+
                                                                                '<span class="' + badge + '">' + label + '</span>' +
                                                                            '</div>' +
                                                                        '</div>' +
                                                                    '</div>' +
                                                                '</div>' +
                                                            '</div>' +
                                                        '</div>';
                                                        }
                                                    } else{
                                                        innerHTML += '<div class="col-xl-4 col-xxl-7 col-sm-7 comp-content">' +
                                                            '<div class="loadmore-content">' +
                                                                '<div class="row" id="FeaturedCompaniesContent">' +
                                                                    '<div class="col-xl-12 col-sm-6 mt-4">' +
                                                                        '<div class="d-flex">' +
                                                                            '<span>' +
                                                                                '<img src="https://img.icons8.com/external-flat-icons-pack-pongsakorn-tan/64/000000/external-company-labor-day-flat-icons-pack-pongsakorn-tan.png"/>' +
                                                                            '</span>' +
                                                                            '<div class="featured">'+
                                                                                '<h4 class="fs-5 mb-1">' + content_data.comp_name + '</h4>'+
                                                                                '<span class="' + badge + '">' + label + '</span>' +
                                                                            '</div>' +
                                                                        '</div>' +
                                                                    '</div>' +
                                                                '</div>' +
                                                            '</div>' +
                                                        '</div>';
                                                    }
                                                    /* *******  company lists  ******* */
                                                innerHTML += '</div>' +
                                                /* *** progress('20220222','2022025') *** */
                                                '<div class="row align-items-center m-l-1">' +
                                                    '<h6 class="fs-20 mb-3">?????? ??????</h6>' +
                                                    '<div >' +
                                                        '<div class="progress progress-sm">' +
                                                            '<div class="progress-bar bg-blue " style="width: ' + process_percent + '%; height:13px;" role="progressbar">' +
                                                                '<span class="sr-only">' + process_percent + '% Complete</span>' +
                                                            '</div>' +
                                                        '</div>' +
                                                        '<div class="d-flex align-items-end mt-2 pb-4 justify-content-between" style="position:relative">' +
                                                            '<span class="fs-14 font-w500">?????? ????????? <br/>' + dateformat(content_data.work_str_date) + '</span>' +
                                                            '<span class="fs-14 font-w500" style="text-align:right;">?????? ?????? ????????? <br/>' + dateformat(content_data.work_end_date) + '</span>' +
                                                            '<span class="fs-16 progress-fs" style="position:absolute;top:-50px; right:0;"><span class="text-black pe-2"></span>' + process_percent + '%</span>' +
                                                        '</div>' +
                                                    '</div>' +
                                                '</div>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>';
                    }
                    $('.data-row').html(innerHTML);
                }

            }
        });
    }
    $('#searchBtn').on('click',function(){
        $('.data-row').html('');
        doSearch(
          $('#dateFrom').val().replace(/\-/g,''),
          $('#dateTo').val().replace(/\-/g,'')
        );
    })
    doSearch(
      $('#dateFrom').val().replace(/\-/g,''),
      $('#dateTo').val().replace(/\-/g,'')
    );
});
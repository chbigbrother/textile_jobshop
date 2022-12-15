function dateformat(value) {
    var year = value.substring(0, 4);
    var month = value.substring(4, 6);
    var day = value.substring(6, 8);
    var date = year + '-' + month + '-' + day;
    return date;
}

// 전송 클릭 시 이벤트
function sendSchedule() {
    $('#confirmDataModal').modal('show');
    var orderInfo = new Array();
    for (var i = 0; i < $('.checkbox').length; i++) {
        if ($('.checkbox').eq(i).val() == 'Y') {
            orderInfo.push($('.checkbox').eq(i).parent().siblings('.order_id').val());
        }
    }
    var innerHTML = '';
    for(var i=0; i<orderInfo.length; i++){
        var thisOrders = orderInfo[i].split(',');
        for (var j=0; j<thisOrders.length; j++){
            innerHTML += '<div class="row sch-pknu-modal-row">' +
                            '<div class="col-md-3"><label class="pt-2">주문 정보</label></div>' +
                                '<div class="col-md-9" id="orderInfoModal">' +
                                    '<input type="text" class="form-control" id="schInfo" aria-describedby="emailHelp" readonly="readonly" value="' + thisOrders[j]+ '"  />' +
                                '</div>' +
                         '</div>' +
                        '<div class="row sch-pknu-modal-row">' +
                            '<div class="col-md-3"><label class="pt-2">제안 가격</label></div>' +
                            '<div class="col-md-9" id="offerPriceModal">' +
                                '<input type="text" class="form-control offeredPrice" aria-describedby="emailHelp" value=""  />' +
                            '</div>'+
                        '</div>';
        }
    }
    $('#priceModalBody').html(innerHTML);
}

// 확정 전달 클릭 시 이벤트
function confirmSend(){
    Swal.fire({
        icon: 'question',
        title: '스케쥴을 확정하시겠습니까?',
        showDenyButton: true,
        confirmButtonText: '네',
        denyButtonText: `아니오`,
    }).then((result) => {
        if (result.isConfirmed) {
            $('#css-loader').addClass("is-active");
            var order = new Array();
            var sch_id = new Array();
            for (var i = 0; i < $('.checkbox').length; i++) {
                if ($('.checkbox').eq(i).val() == 'Y') {
                    order.push($('.checkbox').eq(i).parent().siblings('.order_id').val());
                    sch_id.push($('.checkbox').eq(i).parent().siblings('.sch_id').val());
                }
            }
            var price = new Array();
            for (var i=0; i<$('.offeredPrice').length; i++){
                price.push($('.offeredPrice').eq(i).val());
            }

            var obj = new Object();
            obj.type = 'company';
            obj.order_list = order;
            obj.price_list = price;
            obj.sch_list = sch_id;
            $.ajax({
                url: '/textile/schedule/fixed/order/', /* "{% url 'schedule:fixed_order' %}",*/
                method: 'POST',
                dataType: "json",
                type:'json',
                contentType: 'application/json',
                data: JSON.stringify(obj),
            }).done(function(response) {
                $('#css-loader').removeClass("is-active");
                location.reload();
                $('#activationSettingModal').modal('hide');
            })
        }
    });
}


// 새로 생성 버튼 클릭 시 이벤트
function removeSchedule() {
    // 기존의 확정된 스케줄 삭제
    Swal.fire({
        icon: 'question',
        title: '스케쥴을 새로 생성하시겠습니까?',
        showDenyButton: true,
        confirmButtonText: '네',
        denyButtonText: `아니오`,
    }).then((result) => {
        if (result.isConfirmed) {
            $('#css-loader').addClass("is-active");
            // var order = new Array();
            var sch = new Array();
            for (var i = 0; i < $('.order_id').length; i++) {
                // order.push($('.order_id').eq(i).val());
                sch.push($('.sch_id').eq(i).val());
            }
            $.ajax({
                url: '/textile/schedule/delete/order/',/*"{% url 'schedule:delete_order' %}",*/
                method: 'POST',
                dataType: "json",
                contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                data: {
                    'sch_list[]': sch
                },
            }).done(function(response) {
                $('#css-loader').removeClass("is-active");
                location.reload();
            })
        }
    });
}

// 섬유공정스케줄실행 클릭 시 이벤트
function activate() {
    $('#css-loader').addClass("is-active");
    var selected_fac_list = new Array();
    for(var i=1; i<$('.ordamt').length+1; i++){
        var selected_fac = new Array();
        $('.availfacnum_' + i).find(':selected').each(function(j){
            selected_fac.push($('.availfacnum_' + i).find(':selected')[j].innerText);
        });
        selected_fac_list.push(selected_fac);
    }
    var selected_ord_list = new Array();
    var selected_amt_list = new Array();
    var selected_fac_num_list = new Array();
    var selected_opt_num_list = new Array();
    var arr = new Array();
    var sch_ord_id = new Array();
    var str_arr = new Array();
    $('.ordamt').each(function(i){
        console.log($('.ordamt')[i]);
        var cnt = $('.ordamt')[i].classList.length-1;
        var prod_name = $('.ordamt')[i].id;
        selected_ord_list.push(prod_name);
        var amt = $('.ordamt')[i].classList[cnt];
        amt = amt.split('_');
        amt = amt[1];
        selected_amt_list.push(amt);
    });
    $('.setMachineNum').each(function(i){
        selected_fac_num_list.push($('.setMachineNum')[i].value);
    });

    /* *************************
       작업 기한 Array
     ************************* */
    $('.estDate').each(function(i, elem){
        arr.push($(this).val());
    });

    /* *************************
       작업시작일자 Array
     ************************* */
    $('.strDate').each(function(i, elem){
        str_arr.push($(this).val());
    });

    $('.sch_ord_id').each(function(i, elem){
        sch_ord_id.push($(this).val());
    })

    var obj = new Object();
    obj.ord_id = sch_ord_id;
    obj.ord = selected_ord_list;
    obj.fac = selected_fac_list;
    obj.amt = selected_amt_list;
    obj.work_str_date = str_arr; // $('#strDate').val();
    obj.work_exp_date = arr; // $('#estDate').val();

    $.ajax({
        url: '/textile/schedule/graph/csv/generate/', /* "{% url 'schedule:generate_data' %}",*/
        data: JSON.stringify(obj),
        type: 'json',
        contentType: 'application/json',
        method: "POST",
    }).done(function(response) {
        $('#css-loader').removeClass("is-active");
        location.reload();
    })
}

$(function() {
    var bodyClick = false;
    const today = moment();
    // 검색 날짜 init
    flatpickr("#dateTo", {
        locale: Flatpickr.l10ns.ko,
        enableTime: false,
        dateFormat: "Y-m-d",
        disableMobile: true,
        defaultDate: [today.format('YYYY-MM-DD')]
    });
    // 검색 날짜 init
    flatpickr("#dateFrom", {
        locale: Flatpickr.l10ns.ko,
        enableTime: false,
        dateFormat: "Y-m-d",
        disableMobile: true,
        defaultDate: $("#dateFrom").val()
    });
    $('#activationSetting').on('click', function() {
        $('#activationSettingModal').modal('show');
    })
    $(document).ready(function() {
        const today = moment();
        // 검색 날짜 init
        flatpickr("#estDate", {
            locale: Flatpickr.l10ns.ko,
            enableTime: false,
            dateFormat: "Y-m-d",
            disableMobile: true,
            defaultDate: [today.format('YYYY-MM-DD')]
        });
        $("#ordDateTo").val([today.format('YYYY-MM-DD')]);
        $("#orderDateFrom").val($("#dateFrom").val());

        orderDraw();
        // facilityDraw();
    })
    // 주문일자에 따른 수주 리스트 불러오기 START
    $('#ordDateFrom').on('change', function() {
        orderDraw();
    });
    $('#ordDateTo').on('change', function() {
        orderDraw();
    });
    function clickBodyEvent(event) {
        var target = event.target;
        if (target == event.currentTarget.querySelector(".modal-body")) {
            $('#selectOrder_old').html('');

            var selected_ord = $('#divSelectOrder_old .ms-drop ul li.selected');
            if (selected_ord.length > 1) {
                $('#orderSelectDiv').css('overflow', 'scroll');
                $('#orderSelectDiv').css('overflow-x', 'hidden');
                $('#orderSelectDiv').css('height', '398px');
            }

            var innerHTML = '';
            for (var i = 0; i < selected_ord.length; i++) {
                var amt = selected_ord[i].className.split('_');
                if(amt.length > 1){
                    var amt_cnt = amt[0]; // 수량
                    var amt_val = amt[1]; // 기계 대수
                    var appendHTML = facilityDraw(i);
                    if (typeof selected_ord[i].value != 'undefined') {
                        innerHTML += '<div class="col-xl-13" id="accordion">'+
                                    '<div class="accordion accordion-header-bg accordion-bordered" id="accordion">'+
                                        '<div class="accordion-item">'+
                                            '<div class="accordion-header rounded-lg" id="collapse-' + i + '" data-bs-toggle="collapse" data-bs-target="#collapse' + i + '" aria-controls="collapse' + i + '"   aria-expanded="true"  role="button">'+
                                                '<span class="accordion-header-icon"></span>'+
                                                '<span class="accordion-header-text ordamt ordamt_' + amt_cnt + '" id="' + amt[2] + '">' + selected_ord[i].innerText + '</span>'+
                                                '<span class="accordion-header-indicator"></span>'+
                                            '</div>';
                                            if(i == 0){
                                                innerHTML += '<div id="collapse' + i + '" class="collapse accordion__body show" aria-labelledby="accord-7One" data-bs-parent="#accordion">';
                                            } else {
                                                innerHTML += '<div id="collapse' + i + '" class="collapse accordion__body" aria-labelledby="accord-7One" data-bs-parent="#accordion">';
                                            }
                                   innerHTML += '<div class="accordion-body-text">'+
                                                    '<label class="pt-2" style="margin-right:2.2rem;">기계 대수</label>'+
                                                    appendHTML +
                                                    '<label class="pt-3" style="margin-right:2.2rem;">작업시작일자</label>' +
                                                    '<input class="form-control text-center strDate" id="strDateId_' + i + '" type="date" name="dateFrom" />'+
                                                    '<label class="pt-3" style="margin-right:2.2rem;">작업 기한</label>'+
                                                    '<input class="form-control text-center estDate" id="estDateId_' + i + '" type="date" name="dateTo"/>'+
                                                '</div>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>';
                    }
                }
            }
            $('#divSelectOrder_old').html(innerHTML);
            $(".estDate").val([today.format('YYYY-MM-DD')]);
            $(".strDate").val([today.format('YYYY-MM-DD')]);

            $('#divSelectOrder_old').attr('id', 'divSelectOrder');
            $(".availfacnum").multipleSelect({
                filter: true
            });
        }

    }
    var result_data;
    // 기간 내 처리 가능 오더 조회
    function orderSearch(from, to, orderInfo) {
        from = from.replace('-', '').replace('-', '');
        to = to.replace('-', '').replace('-', '');
        var obj = new Object();
        obj.dateFrom = from;
        obj.dateTo = to;
        obj.orderInfo = orderInfo;
        $.ajax({
            url: '/textile/order/list/search/', /*"{% url 'order:order.order_list_search' %}",*/
            method: 'GET',
            dataType: 'json',
            async: false,
            data: JSON.stringify(obj),
            contentType: 'application/json',
            processData: false,
            success: function(result) {
                result_data = result;
            }

        });
        return result_data;
    }

    function orderDraw() {
        $('#selectOrder').html('');
        var orderInfo = new Array();
        if (bodyClick == true){
            for (var i = 0; i < $('.checkbox').length; i++) {
                if ($('.checkbox').eq(i).val() == 'Y') {
                    orderInfo.push($('.checkbox').eq(i).parent().siblings('.order_id').val());
                }
            }
        }

        var result = orderSearch($('#ordDateFrom').val(), $('#ordDateTo').val(), orderInfo);
        if (result.length > 0) {
            var innerHTML = '';
            var ordHTML = '';
            innerHTML += '<select class="form-control" name="select" multiple="multiple" id="selectOrder">';
            for (var i = 0; i < result.length; i++) {
                if (typeof result[i] !== 'undefined') {
                    innerHTML += '<option id="'+ i + '" class="' + result[i].amount + "_" + result[i].avail_fac_cnt + "_" + result[i].prod_name + '_" value="' + result[i].prod_name + '">' + result[i].cust_name + '_' + result[i].prod_name + '_' + result[i].amount + ' yd' +
                    ' 요청기한 ' + result[i].exp_date + ' </option>';
                    ordHTML += '<input type="hidden" class="sch_ord_id" value="' + result[i].order_id + '">';
                }
            }
        } else {
            var innerHTML = '<input type="text" class="form-control" placeholder="해당일에 주문데이터가 없습니다." value="" readonly="readonly" />';
        }
        $('#divSelectOrder_old').html(innerHTML);
        $("#selectOrder").multipleSelect({
            filter: true
        });
        $('.ord_hidden').append(ordHTML);
        return;
    }
    // 주문일자에 따른 수주 리스트 불러오기 END

    $('#divSelectOrder_old').on('click', function(event) {
        bodyClick = true;
        var body = document.querySelector("body");
        body.addEventListener('click', clickBodyEvent);
    });

    // 작업 시작 일자에 따른 사용 가능 기계 리스트 불러오기 START
    function facilityDraw(num) {
        // $('#divSelectFac').html('');
        var obj = new Object();
        obj.strDate = $("#strDate").val();
        var innerHTML = '';
        var data = '';
        $.ajax({
            url: '/textile/company/avail/facility/', /*"{% url 'company:company.comp_avail_facility' %}",*/
            method: 'GET',
            dataType: 'json',
            async: false,
            data: JSON.stringify(obj),
            contentType: 'application/json',
            processData: false,
            success: function(result) {
                data = result;
            }
        });
        if (data.length > 1) {
            innerHTML += '<div class="col-md-6 form-control">' +
                            '<select class="availfacnum availfacnum_' + num + '" name="select" multiple="multiple" id="availfacnum" style="width:100%;">';
            for (var i = 0; i < data.length; i++) {
                if (typeof data[i] !== 'undefined') {
                    innerHTML += '<option value="' + data[i] + '" selected>' + data[i] + ' 호기</option>';
                }
            }
        } else {
            var innerHTML = '<input type="text" class="form-control" placeholder="사용가능한 설비가 없습니다." value="" readonly="readonly" />';
        }
            innerHTML += '</select></div> ';
        return innerHTML;
    }

    $('#availfacnum').on('change', function() {
        var facnum = $('#availfacnum').val();
        var order = $('#selectOrder').val();
        var innerHTML = '<thead>' +
            '<tr>' +
            '<th></th>';
        for (var i = 1; i <= facnum; i++) {
            innerHTML += '<th>machine ' + i + '</th>';
        }
        innerHTML += '</tr>' +
            '</thead>' +
            '<tbody>';
        for (var i = 0; i < order.length; i++) {
            innerHTML += '<tr> <td>' + order[i] + '</td>';
            for (var j = 1; j <= facnum; j++) {
                innerHTML += '<td><input type="text" style="border:none; width:50px;"/></td>';
            }
            innerHTML += '</tr>';
        }
        $('#dataTable').html(innerHTML);
        $('#processingdataTable').html(innerHTML);
    })


    var ctx = document.getElementById("myAreaChart");
    var chartset = false;
    var xmin = 0;
    var xmax = 0;
    var ymin = 0;
    var ymax = 0;
    var enddate = new Array();
    let date = new Date();
    $.ajax({
        url: '/textile/schedule/graph/draw/', /* "{% url 'schedule:draw_graph' %}",*/
        method: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        processData: false,
        success: function(result) {
            if(result.length>0){
                var dataset = new Array();
                var annotationset = new Array();
                var x_min = result[0].work_str_date;
                var y_min = result[0].y_axis_1;
                for (var i = 0; i < result.length; i++) {
                    enddate = new Date(result[i].work_end_date);
                    var xmin = new Date(result[i].work_str_date);
                    var x_axis_1 = new Date(xmin.setDate(xmin.getDate() + result[i].x_axis_1));
                    var x_axis_2 = result[i].x_axis_2 - result[i].x_axis_1;
                    if (y_min > result[i].y_axis_1) {y_min = result[i].y_axis_1;}
                    if (xmax < result[i].x_axis_2) {xmax = result[i].x_axis_2;}
                    if (ymax < result[i].y_axis_1) {ymax = result[i].y_axis_1;}
                    dataset.push({
                        label: result[i].prod_name,
                        backgroundColor: "rgba(78, 115, 223, 0.05)",
                        borderColor: result[i].sch_color,
                        fill: false,
                        responsive: true,
                        borderWidth: 15,
                        pointRadius: 0,
                        data: [{
                            x: x_axis_1,
                            y: result[i].y_axis_1,
                        }, {
                            x: new Date(xmin.setDate(xmin.getDate() + x_axis_2)),
                            y: result[i].y_axis_1,
                        }]
                    });

                    annotationset.push({
                        drawTime: "afterDatasetsDraw",
                        type: "line",
                        mode: "vertical",
                        scaleID: "x-axis-0",
                        value: enddate,
                        borderWidth: 1,
                        borderColor: result[i].sch_color,
                        label: {
                            content: result[i].prod_name + " deadline : " + (enddate.getMonth() + 1) + "/" + enddate.getDate() + "",
                            enabled: true,
                            position: "top",
                            backgroundColor: "rgba(160,170,174,100)",
                        }
                    });


                }

                // chart.js 그리기
                var scatterChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        datasets: dataset
                    },
                    options: {
                        // y축 빨간선 표시
                        annotation: {
                            annotations: annotationset
                        }, // y축 빨간선 표시
                        animation: {
                            onComplete: function() {
                                var ctx = this.chart.ctx;
                                var cht = this.chart;
                                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontFamily, 'light', Chart.defaults.global.defaultFontFamily);
                                ctx.fillStyle = "#466964";
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'bottom';

                                this.data.datasets.forEach(function(dataset, i) {
                                    var meta = cht.controller.getDatasetMeta(i);
                                    var data = dataset.label;
                                    var arr = new Array();
                                    arr.push(data);
                                    meta.data.forEach(function(bar, index){
                                        var label = arr[index];
                                        if (typeof label == 'undefined') {label = ''}
                                        ctx.fillText(label, bar._model.x, bar._model.y-5);
                                    })

                                });

                            }
                        },
                        legend: {
                            display: false
                        },
                        scales: {
                            xAxes: [{
                                type: 'time',
                                position: 'bottom',
                                scaleLabel: {
                                    display: true,
                                    labelString: 'dates'// '날짜'
                                },
                                // ticks: {
                                time: {
                                    unit: 'day',
                                    unitStepSize: 1,
                                    displayFormats: {
                                        'day': 'MM / DD'
                                    }
                                    // min: x_min,
                                    // max: xmin + (xmax/10),
                                    // suggestedMin: 1,
                                    // maxRotation: 0,
                                    // stepSize: 1
                                }
                            }],
                            yAxes: [{
                                scaleLabel: {
                                    display: false
                                },
                                scaleLabel: {
                                    display: true,
                                    labelString: 'machine number' // '기계 번호'
                                },
                                ticks: {
                                    beginAtZero: true,
                                    stepSize: 1,
                                    min: y_min - 1,
                                    max: ymax + 1
                                }
                            }]
                        },
                        pan: {
                            enabled: true,
                            mode: 'x',
                        },
                        zoom: {
                            enabled: true,
                            mode: 'x',
                        },
                    },
                });
            }
            /* ******************************************************** */
            $.ajax({
                url: '/textile/schedule/avail/comp/', /* "{% url 'schedule:available_comp' %}",*/
                method: 'GET',
                dataType: 'json',
                contentType: 'application/json',
                processData: false,
                success: function(result) {
                    $.ajax({
                        url: '/textile/schedule/confirmed/order/',/* "{% url 'schedule:confirmed_order' %}", */
                        method: 'GET',
                        dataType: 'json',
                        contentType: 'application/json',
                        processData: false,
                        success: function(data) {
                            var innerHTML = '';
                            if (data.length > 0) {
                                for (var i = 0; i < data.length; i++) {
                                    if (data[i][0].use_yn == 'Y') {
                                        $('#activationSetting').remove();
                                        $('#sendSchedule').remove();
                                        $('#sendBtn').html('<a href="#" onclick="removeSchedule()" id="removeSchedule"' +
                                            'class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">' +
                                            '<i class="fas fa-plus-square"></i>&nbsp 초기화</a>');
                                        /* 추후 삭제 */
                                        var prod_name = result[i].prod_id.toString();
                                        var orderid = result[i].order_id_id.toString();
                                        /* 추후 삭제 */

                                        var date = result[i].sch_id.toString()
                                        var year = date.substring(3, 7);
                                        var month = date.substring(7, 9);
                                        var day = date.substring(9, 11);
                                        date = year + '-' + month + '-' + day;
                                        var count = i + 1;
                                        innerHTML += '<tr>' +
                                            '<input type="hidden" class="order_id" value="' + result[i].order_id + '" />' +
                                            '<input type="hidden" class="sch_id" value="' + result[i].sch_id + '" />' +
                                            '<td scope="row">' + count + '</td>' +
                                            '<td>' + date + '</td>' +
                                            '<td>' + orderid + '</td>' +
                                            '<td>' + prod_name + '</td>' +
                                            '<td><div style="width:1rem; height:1rem; background-color:' + result[i].sch_color + '"></div></td>' +
                                            '<td><div class="checkbox" id="accept-' + count + '" style="font-weight:bold; color:#2e59d9;" />확정</td>' +
                                            '</tr>';
                                    } else {
                                        for (var i = 0; i < result.length; i++) {
                                            var prod_name = result[i][0].prod_id.toString();
                                            var orderid = result[i][0].order_id_id.toString();
                                            var date = result[i][0].sch_id.toString();
                                            // var date = result[i].schedule[0].sch_id.toString();
                                            var year = date.substring(3, 7);
                                            var month = date.substring(7, 9);
                                            var day = date.substring(9, 11);
                                            date = year + '-' + month + '-' + day;
                                            var count = i + 1;
                                            innerHTML += '<tr>' +
                                                '<input type="hidden" class="order_id" value="' + orderid + '" />' +
                                                '<input type="hidden" class="sch_id" value="' + result[i][0].sch_id + '" />' +
                                                '<td scope="row">' + count + '</td>' +
                                                '<td>' + date + '</td>' +
                                                '<td>' + orderid + '</td>' +
                                                '<td>' + prod_name + '</td>' +
                                                '<td><div style="width:1rem; height:1rem; background-color:' + result[i][0].sch_color + '"></div></td>' +
                                                '<td><input class="checkbox" id="accept-' + count + '" type="checkbox" checked="checked" value="Y" name="check"/></td>' +
                                                '</tr>';
                                        }
                                    }
                                }
                            } else {
                                for (var i = 0; i < result.length; i++) {
                                    /* 추후 삭제 */
                                    var prod_name = result[i].prod_id.toString();
                                    var orderid = result[i].order_id_id.toString();
                                    /* 추후 삭제 */
                                    var date = result[i].sch_id.toString();
                                    var year = date.substring(3, 7);
                                    var month = date.substring(7, 9);
                                    var day = date.substring(9, 11);
                                    date = year + '-' + month + '-' + day;
                                    var count = i + 1;
                                    innerHTML += '<tr>' +
                                        '<input type="hidden" class="order_id" value="' + orderid + '" />' +
                                        '<input type="hidden" class="sch_id" value="' + result[i].sch_id + '" />' +
                                        '<td scope="row">' + count + '</td>' +
                                        '<td>' + date + '</td>' +
                                        '<td>' + orderid + '</td>' +
                                        '<td>' + prod_name + '</td>' +
                                        '<td><input class="checkbox" id="accept-' + count + '" type="checkbox" checked="checked" value="Y" name="check"/></td>' +
                                        '</tr>';
                                }
                            }
                            $('#order_body').html(innerHTML);
                        } /* data ajax */
                    }).done(function(d) {
                        $('input:checkbox[name="check"]').on('change', function() {
                            if ($(this).val() == 'Y') {
                                $(this).val('N');
                            } else {
                                $(this).val('Y');
                            }
                        })
                    });
            } /* result ajax */
        });


        }
    });


    // ******************************************************************************************************* //
    // schedule_history
    $.ajax({
        url: "/textile/schedule/history/", /* "{% url 'schedule:schedule_history' %}",*/
        method: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        processData: false,
        success: function(result) {
            var innerHTML = '';
            for (var i = 0; i < result.length; i++) {
                /* 추후 삭제 */
                var orderid = result[i].schedule[0].order_id_num.toString();
                var date = result[i].schedule[0].sch_id.toString();
                var year = date.substring(3, 7);
                var month = date.substring(7, 9);
                var day = date.substring(9, 11);
                date = year + '-' + month + '-' + day;

                /* 추후 삭제 */
                var count = i + 1;
                if (result[i].use_yn == 'Y') {
                    innerHTML += '<tr>' +
                        '<input type="hidden" class="fixed_order_id" value="' + result[i].schedule[0].order_id + '" />' +
                        '<td scope="row">' + count + '</td>' +
                        '<td>' + date + '</td>' +
                        '<td>' + orderid.split('.')[0] + '</td>' +
                        '<td><div style="width:1rem; height:1rem; background-color:' + result[i].schedule[0].sch_color + '"></div></td>' +
                        '<td>확정</td>' +
                        '</tr>';
                } else {
                    innerHTML += '<tr>' +
                        '<input type="hidden" class="fixed_order_id" value="' + result[i].schedule[0].order_id + '" />' +
                        '<td scope="row">' + count + '</td>' +
                        '<td>' + result[i].schedule[0].created_at + '</td>' +
                        '<td>' + orderid.split('.')[0] + '</td>' +
                        '<td><div style="width:1rem; height:1rem; background-color:' + result[i].schedule[0].sch_color + '"></div></td>' +
                        '<td>미사용</td>' +
                        '</tr>';
                }

            }
            $('#fixed_order_body').html(innerHTML);
        }
    });
    $('#searchBtn').on('click', function() {
        doSearch(
            $('#dateFrom').val().replace(/\-/g, ''),
            $('#dateTo').val().replace(/\-/g, '')
        );
    })

    function doSearch(dateFrom, dateTo) {
        $.when(
            $.ajax({
                url: "{% url 'schedule:schedule_history' %}"
            })
        ).then(function(_data) {
            for (var idx in _data) {
                console.log(_data);
            }
            $('#css-loader').removeClass("is-active");
        })
    }
});
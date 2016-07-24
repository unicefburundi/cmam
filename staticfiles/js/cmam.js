$(document).ready(function(){
    $('.camebu').hide();
    $('.district').hide();
    $('.cds').hide();
    $('select[id=id_product]').change(function(){
        product_id = $(this).val();
        if (product_id) {
            request_url = '/cmam/products/' + product_id + '/';
            $.ajax({
                url: request_url,
                success: function(data){
                    $('.camebu').show();
                    $('#unites').html('<strong >' + data.general_measuring_unit +'</strong>');
                }
            });
            $('select[id=id_province]').change(function(){
                province_id = $(this).val();
                if (province_id) {
                    request_url = '/bdiadmin/get_district/' + province_id + '/';
                    $.ajax({
                        url: request_url,
                        success: function(data){
                        $('select[name=district]').html('<option value="" selected="selected">---------</option>'); // remove the value from the input
                        $('.district').show();
                        data = JSON.parse(data);
                        $.each(data, function(key, value){
                            for (var i in value) {
                            }
                            $.each(value, function(key, value){
                                $('select[name=district]').append('<option value="' + key + '">' + value +'</option>');
                            });
                        });
                    }
                });
                }
                else {
                $('.cds').hide();
                $('select[name=district]').html('<option value="" selected="selected">---------</option>'); // remove the value from the input
            } //<---- move it here
        });
            $('select[id=id_district]').change(function(){
                $('.cds').show();
            });
        } else {
            $('.camebu').hide();
            $('.district').hide();
            $('.cds').hide();
        }

    });
});
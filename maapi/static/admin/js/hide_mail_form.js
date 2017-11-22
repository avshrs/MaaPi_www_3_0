django.jQuery(document).ready(function()
  {
  if(django.jQuery('#id_mail_condition_min_e').val()==='2'){
    django.jQuery(".field-mail_condition_min").show();
  }
  else{
    django.jQuery(".field-mail_condition_min").hide();
  }


  django.jQuery('#id_mail_condition_min_e').change(function(){
    var selected_option =   django.jQuery('#id_mail_condition_min_e').val();

    if (selected_option === '2') {
      django.jQuery('.field-mail_condition_min').show(200);
    }
    if (selected_option != '2') {
      django.jQuery(".field-mail_condition_min").hide(200);
    }
  })
///////////////////////////////////////////////////////////
if(django.jQuery('#id_mail_condition_max_e').val()==='2'){
  django.jQuery(".field-mail_condition_max").show();
}
else{
  django.jQuery(".field-mail_condition_max").hide();
}


django.jQuery('#id_mail_condition_max_e').change(function(){
  var selected_option =   django.jQuery('#id_mail_condition_max_e').val();

  if (selected_option === '2') {
    django.jQuery('.field-mail_condition_max').show(200);
  }
  if (selected_option != '2') {
    django.jQuery(".field-mail_condition_max").hide(200);
  }
})
///////////////////////////////////////////////////////////

})

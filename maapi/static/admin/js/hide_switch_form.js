django.jQuery(document).ready(function(){
  //---------------------------minimal
  if(django.jQuery('#id_switch_value_min_e').val()==='2'){
    django.jQuery(".field-switch_value_min").show();
    django.jQuery(".field-switch_reference_sensor_min_e").show();
    django.jQuery(".field-switch_reference_sensor_min").show();

    }
  else{
    django.jQuery(".field-switch_value_min").hide();
    django.jQuery(".field-switch_reference_sensor_min_e").hide();
    django.jQuery(".field-switch_reference_sensor_min").hide();

    }
    if(django.jQuery('#id_switch_turn_on_at_sensor_e').val()==='2'){
      django.jQuery(".field-switch_turn_on_at_sensor").show();
      django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").show();
      django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").show();

      }
    else{
      django.jQuery(".field-switch_turn_on_at_sensor").hide();
      django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").hide();
      django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").hide();

      }

      if(django.jQuery('#id_switch_turn_on_at_sensor_value_min_e').val()==='2'){
        django.jQuery(".field-switch_turn_on_at_sensor_value_min").show(200);

      }
      else{  django.jQuery(".field-switch_turn_on_at_sensor_value_min").hide(200);}


      if(django.jQuery('#id_switch_turn_on_at_sensor_value_max_e').val()==='2'){
        django.jQuery(".field-switch_turn_on_at_sensor_value_max").show(200);

      }  else{  django.jQuery(".field-switch_turn_on_at_sensor_value_max").hide(200);}
    if(django.jQuery('#id_switch_turn_on_at_sensor_e').val()==='2'){
      django.jQuery(".field-switch_turn_on_at_sensor").show();
      django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").show();
      django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").show();

      }
    else{
      django.jQuery(".field-switch_turn_on_at_sensor").hide();
      django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").hide();
      django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").hide();

      }

      django.jQuery('#id_switch_turn_on_at_sensor_e').change(function(){
          if (django.jQuery('#id_switch_turn_on_at_sensor_e').val() === '2') {
            django.jQuery(".field-switch_turn_on_at_sensor").show(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").show(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").show(200);

            if(django.jQuery('#id_switch_turn_on_at_sensor_value_min_e').val()==='2'){
              django.jQuery(".field-switch_turn_on_at_sensor_value_min").show(200);

            }
            if(django.jQuery('#id_switch_turn_on_at_sensor_value_max_e').val()==='2'){
              django.jQuery(".field-switch_turn_on_at_sensor_value_max").show(200);

            }
          }
          else {
            django.jQuery(".field-switch_turn_on_at_sensor").hide(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_min_e").hide(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_max_e").hide(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_min").hide(200);
            django.jQuery(".field-switch_turn_on_at_sensor_value_max").hide(200);

          }
        })
  django.jQuery('#id_switch_value_min_e').change(function(){
      if (django.jQuery('#id_switch_value_min_e').val() === '2') {
        django.jQuery(".field-switch_value_min").show(200);
        django.jQuery(".field-switch_reference_sensor_min_e").show(200);
        django.jQuery(".field-switch_reference_sensor_min").show(200);
      }
      else {
        django.jQuery(".field-switch_value_min").hide(200);
        django.jQuery(".field-switch_reference_sensor_min_e").hide(200);
        django.jQuery(".field-switch_reference_sensor_min").hide(200);
      }
    })



    django.jQuery('#id_switch_turn_on_at_sensor_value_min_e').change(function(){
        if (django.jQuery('#id_switch_turn_on_at_sensor_value_min_e').val() === '2') {
          django.jQuery(".field-switch_turn_on_at_sensor_value_min").show(200);

        }
        else {

          django.jQuery(".field-switch_turn_on_at_sensor_value_min").hide(200);
        }
      })



      django.jQuery('#id_switch_turn_on_at_sensor_value_max_e').change(function(){
          if (django.jQuery('#id_switch_turn_on_at_sensor_value_max_e').val() === '2') {
            django.jQuery(".field-switch_turn_on_at_sensor_value_max").show(200);

          }
          else {

            django.jQuery(".field-switch_turn_on_at_sensor_value_max").hide(200);
          }
        })


  django.jQuery('#id_switch_reference_sensor_min_e').change(function(){
        if (django.jQuery('#id_switch_reference_sensor_min_e').val() === '2') {
            django.jQuery(".field-switch_reference_sensor_min").show(200);
        }
        else {
          django.jQuery(".field-switch_reference_sensor_min").hide(200);
        }
      })


/////-------------------maximal
if(django.jQuery('#id_switch_value_max_e').val()==='2'){
  django.jQuery(".field-switch_value_max").show();
  django.jQuery(".field-switch_reference_sensor_max_e").show();
  django.jQuery(".field-switch_reference_sensor_max").show();

  }
else{
  django.jQuery(".field-switch_value_max").hide();
  django.jQuery(".field-switch_reference_sensor_max_e").hide();
  django.jQuery(".field-switch_reference_sensor_max").hide();
  }


django.jQuery('#id_switch_value_max_e').change(function(){
    if (django.jQuery('#id_switch_value_max_e').val() === '2') {
      django.jQuery(".field-switch_value_max").show(200);
      django.jQuery(".field-switch_reference_sensor_max_e").show(200);
      django.jQuery(".field-switch_reference_sensor_max").show(200);
    }
    else {
      django.jQuery(".field-switch_value_max").hide(200);
      django.jQuery(".field-switch_reference_sensor_max_e").hide(200);
      django.jQuery(".field-switch_reference_sensor_max").hide(200);
    }
  })

django.jQuery('#id_switch_reference_sensor_max_e').change(function(){
      if (django.jQuery('#id_switch_reference_sensor_max_e').val() === '2') {
          django.jQuery(".field-switch_reference_sensor_max").show(200);
      }
      else {
        django.jQuery(".field-switch_reference_sensor_max").hide(200);
      }
    })

})

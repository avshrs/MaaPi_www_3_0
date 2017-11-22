django.jQuery(document).ready(function()
  {
    if(django.jQuery('#id_math_exec_if_cond_e').val()==='2'){
      django.jQuery(".field-math_exec_cond").show();
      django.jQuery(".field-math_exec_cond_value_min_e").show();
        if(django.jQuery('#id_math_exec_cond_value_min_e').val()==='2')
            {
            django.jQuery(".field-math_exec_cond_value_min").show();
            }
        else
            {
        django.jQuery(".field-math_exec_cond_value_min").hide();
        }
        if(django.jQuery('#id_math_exec_cond_value_max_e').val()==='2')
            {
            django.jQuery(".field-math_exec_cond_value_max").show();
            }
        else
            {
            django.jQuery(".field-math_exec_cond_value_max").hide();
            }
       if(django.jQuery('#id_math_exec_cond_force_value_e').val()==='2')
                {
                django.jQuery(".field-math_exec_cond_force_value").show();
                }
            else
                {
                django.jQuery(".field-math_exec_cond_force_value").hide();
                }
    }
    else{
      django.jQuery(".field-math_exec_cond_force_value").hide();
      django.jQuery(".field-math_exec_cond").hide();
      django.jQuery(".field-math_exec_cond_value_min_e").hide();
      django.jQuery(".field-math_exec_cond_value_min").hide();
      django.jQuery(".field-math_exec_cond_value_max_e").hide();
      django.jQuery(".field-math_exec_cond_value_max").hide();
    }


    django.jQuery('#id_math_exec_if_cond_e').change(function(){
      var selected_option =   django.jQuery('#id_math_exec_if_cond_e').val();

      if (selected_option === '2') {

      django.jQuery(".field-math_exec_cond_force_value_e").show(200);
      django.jQuery(".field-math_exec_cond").show(200);
      django.jQuery(".field-math_exec_cond_value_min_e").show(200);
      if(django.jQuery('#id_math_exec_cond_force_value_e').val()==='2')
               {
               django.jQuery(".field-math_exec_cond_force_value").show();
               }
           else
               {
               django.jQuery(".field-math_exec_cond_force_value").hide();
               }
        if(django.jQuery('#id_math_exec_cond_value_min_e').val()==='2')
            {
            django.jQuery(".field-math_exec_cond_value_min").show();
            }
        else
            {
        django.jQuery(".field-math_exec_cond_value_min").hide();
      }
      if(django.jQuery('#id_math_exec_cond_value_max_e').val()==='2')
          {
          django.jQuery(".field-math_exec_cond_value_max").show();
          }
      else
          {
          django.jQuery(".field-math_exec_cond_value_max").hide();
          }
        django.jQuery(".field-math_exec_cond_value_max_e").show(200);

      }
      if (selected_option != '2') {
        django.jQuery(".field-math_exec_cond_force_value_e").hide(200);
        django.jQuery(".field-math_exec_cond").hide(200);
        django.jQuery(".field-math_exec_cond_value_min_e").hide(200);
        django.jQuery(".field-math_exec_cond_value_min").hide(200);
        django.jQuery(".field-math_exec_cond_value_max_e").hide(200);
        django.jQuery(".field-math_exec_cond_value_max").hide(200);
      }
    })


    django.jQuery('#id_math_exec_cond_value_min_e').change(function(){
      var selected_option =   django.jQuery('#id_math_exec_cond_value_min_e').val();
      if (selected_option === '2') {
        django.jQuery(".field-math_exec_cond_value_min").show(200);
      }
      if (selected_option != '2') {
        django.jQuery(".field-math_exec_cond_value_min").hide(200);
      }
    })
    django.jQuery('#id_math_exec_cond_force_value_e').change(function(){
      var selected_option =   django.jQuery('#id_math_exec_cond_force_value_e').val();
      if (selected_option === '2') {
        django.jQuery(".field-math_exec_cond_force_value").show(200);
      }
      if (selected_option != '2') {
        django.jQuery(".field-math_exec_cond_force_value").hide(200);
      }
    })


    django.jQuery('#id_math_exec_cond_value_max_e').change(function(){
      var selected_option =   django.jQuery('#id_math_exec_cond_value_max_e').val();
      if (selected_option === '2') {
        django.jQuery(".field-math_exec_cond_value_max").show(200);
      }
      if (selected_option != '2') {
        django.jQuery(".field-math_exec_cond_value_max").hide(200);
      }
    })

})

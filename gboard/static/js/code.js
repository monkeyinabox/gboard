// THIS IS OUR JS CODE FILE
// console.log('java script is active');
// window.onload = function () {
//     console.log('page has loaded bitch');
//     document.getElementById('add_task').addEventListener("click",intercept);
//     console.log('dom manipulated')
//     document.getElementById('search-input').addEventListener("change",listFilter);
//     console.log('dom manipulated')
// }

//
//
// function intercept() {
//     alert('action was intercepted');
// }

// SOURCE : https://kilianvalkhof.com/2010/javascript/how-to-build-a-fast-simple-list-filter-with-jquery/
(function ($) {
  // custom css expression for a case-insensitive contains()
  jQuery.expr[':'].Contains = function(a,i,m){
      return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
  };

  function listFilter(filter_list) {
    $(document.getElementById('search-input'))
      .change( function () {
        var filter = $(this).val();
        if(filter) {
          // this finds all links in a list that contain the input,
          // and hide the ones not containing the input while showing the ones that do
          $(filter_list).find("a:not(:Contains(" + filter + "))").parent().slideUp();
          $(filter_list).find("a:Contains(" + filter + ")").parent().slideDown();
        } else {
          $(filter_list).find("li").slideDown();
        }
        return false;
      })
    .keyup( function () {
        // fire the above change event after every letter
        $(this).change();
    });
  }
 //ondomready
 $(function () {
  listFilter($("#filter_list"));
 });
}(jQuery));

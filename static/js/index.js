String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


$(function() {
  
  var jsonData = $('#data').data().name.replaceAll('\'', '"');
  var data = JSON.parse(jsonData);

  $('#user-container').text(data.user.first_name + ' ' + data.user.last_name);

  friendStrings = data.friends.map(function(item) {
  	return item.first_name + ' ' + item.last_name
  })
  friendList = friendStrings.join('<br>')
  console.log(friendStrings)
  $('#friends-container').html(friendList);


});
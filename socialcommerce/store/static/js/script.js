$('.jsSendMessage').click(function(){
    var req = {
        'url': $(this).data('url'),
        'message': $('.message-text__box').val(),
        'store-id': $(this).data('storeId'),
        'user-id': $(this).data('user-id')
    }
    console.log(req)
    console.log($(this).data())
    console.log(req)
    $.post(req['url'], req, function(res){
        console.log(res)
        if (res['status'] == true) {
            $('.message-text__box').val("")
        } 
    });
});

if ($('.jsSendMessage').html() != undefined ) {
    setInterval(function(){
        var req = {
            'url': $('.jsSendMessage').data('url-get'),
            // 'store-id': $('.jsSendMessage').data('storeId'),
        }
        
        $.get(req['url'], function(res){
            var element = $('.message-container');
            var height = $('.message-content__box')[0].scrollHeight;
            for (i=0; i<res.messages.length; i++) {

                var message_item = '<li class="row message-content__item ';
                if (res.messages[i].user_from) {
                    if (res.sender == res.messages[i].user_from.username) {
                        console.log(res.sender + " user from main")
                        message_item += 'left-message__content';
                    } else {
                        console.log(res.sender + " user from else")
                        message_item += 'right-message__content';
                    }
                } else if (res.sender == res.messages[i].store.name) {
                    console.log(res.sender + ' store')
                    message_item += 'left-message__content';
                } else {
                    console.log(res.sender + ' else')
                    message_item += 'right-message__content';
                }
                   
                message_item += ' "><div class="message-content__image">';

                if (res.messages[i].user_from) {
                    // if (res.sender == res.messages[i].user_from.username) {
                        if (res.messages[i].user_from.profile.image) {
                            message_item += '<img class="message-user__img" src="' + res.messages[i].user_from.profile.image + '">';
                        } else {
                            message_item += '<img class="message-user__img" src="/static/img/no-profile-image.png">';
                        }
                    // } else {
                    //     console.log(res.sender + " user from else" + res.messages[i].user_from.username)
                    //     if (res.messages[i].user_from.profile.image) {
                    //         message_item += '<img class="message-user__img" src="' + res.messages[i].user_from.profile.image + '">';
                    //     } else {
                    //         message_item += '<img class="message-user__img" src="/static/img/no-profile-image.png">';
                    //     }
                    // }
                } else if (res.sender == res.messages[i].store.name) {
                    if (res.messages[i].store.image) {
                        message_item += '<img class="message-user__img" src="' + res.messages[i].store.image + '">';
                    } else {
                        message_item += '<img class="message-user__img" src="/static/img/no-store-image.png">';
                    }
                } else {
                    if (res.messages[i].store.image) {
                        message_item += '<img class="message-user__img" src="' + res.messages[i].store.image + '">';
                    } else {
                        message_item += '<img class="message-user__img" src="/static/img/no-profile-image.png">';
                    }
                }

                // else if (res.messages[i].user_to) {
                //     if (res.sender == res.messages[i].user_to.username) {
                //         if (res.messages[i].user_to.profile.image) {
                //             message_item += '<img class="message-user__img" src="' + res.messages[i].user_to.profile.image + '">';
                //         } else {
                //             message_item += '<img class="message-user__img" src="/static/img/no-profile-image.png">';
                //         }
                //     } else {
                //         if (res.messages[i].store.image) {
                //             message_item += '<img class="message-user__img" src="' + res.messages[i].store.image + '">';
                //         } else {
                //             message_item += '<img class="message-user__img" src="/static/img/no-store-image.png">';
                //         }
                //     }
                // }

                message_item += '</div><div class="message-content__content"><h4 class="message-content__user">';

                if (res.messages[i].user_from) {
                    console.log(res.sender + " user from main");
                    // if (res.sender == res.messages[i].user_from.username) {
                    message_item += res.messages[i].user_from.first_name + ' ' + res.messages[i].user_from.last_name;
                    // } else {
                    //     message_item += res.messages[i].store.name
                    // }
                } else {
                    console.log(res.sender + " else store")
                    message_item += res.messages[i].store.name
                }
                message_item += '</h4><div class="message-content__text">' + res.messages[i].content + '</div></div></li>';


                element.append(message_item)
            }
            // if (res.trim() != '') {
            element.scrollTop(height);
            // }
            //     element.scrollTop(height);
            // }
        })
    }, 2000);
}
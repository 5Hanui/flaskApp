$('#searchForm').on('submit', (evt) => { //이벤트 정의하는 함수: on();
    evt.preventDefault();
    console.log('call');
    var param = $('#searchForm').serialize();
    $.ajax({
        url: '/search',      // url
        type: 'post',       // method
        dataType: 'json',   // 응답타입(결과를 어떤타입으로 받을지)
        data: param,        // 데이터(파라미터, 전달데이터, 검색어)
        success: function (res) {
            console.log('성공', res);
            showResult(res);
        },      // 성공
        error: (err) => {
            console.log('실패', err);
        }       // 실패
    });
    return false;
});
function showResult(res) {
    $('#results').empty(); //비우기
    $.each(res, (i, t) => {
        var html = `<div>${t['CODE']} ${t['name']}</div>`;
        console.log(html);
        var kw = $('[name=keyword]').val(); //입력창에 입력된 값을 뽑아줌.
        html = html.replace(kw, `<b>${kw}</b>`) //두꺼운 글씨체
        // div(검색결과가) 1개씩 추가되는 위치 //계속추가되면서 막내가 바뀜..막내를 잡을 수 있다.
        $('#results').append(html);
        // 지금 추가된 요소과 div들 중에 막내라고 측정할 수 있다.
        // 막내를 찾아서 click이벤트를 적용
        // click하면 /info/<code>
        $("#results>div:last").on('click',()=>{
            // alert(t['name']); //팝업
            // 페이지 이동
            document.location.href = '/info/'+t['CODE'];
        });
    }); //res:배열데이터, 
    $('#results b').css('color', 'red');
}
"use strict";
var extension = ""
var file = ""
var LectureData = []
var LectureFormData = new FormData()

$(function () {

    $("#lecturefrom").on('submit', function (e) {
        e.preventDefault(e);
        var form = $(this);
        var formdata = false;

        var forms = form.serializeArray();

        forms.push({
            'name': "file_ext",
            'value': extension,
        })
        forms.push({
            'name': "file",
            'value': file,
        })

        LectureData.push(forms)
        extension = "";
        file = null;

        formdata = new FormData(form[0]);

        form[0].reset()

        addLectureToHtml()
        return false
    })

});

function onLectureFileChange() {
    extension = $('#lectureFileInput').val().replace(/^.*\./, '');
    if (extension == "php") {
    } else {
        file = $('#lectureFileInput')[0].files[0]
        $(this).next('label').text(file);
    }
}

function addLectureToHtml() {
    var tr = "";
    LectureData.forEach((element, index) => {

        tr += ` <tr>
        <td class="text-center">${index+1}</td>
        <td class="cell-ta">${element[0]['value']}</td>
        <td class="text-center">${element[3]['value']}</td>
        <td class="text-center">${element[4]['value']}</td>
        <td class="text-center">${element[1]['value']}</td>
        <td class="text-center">  <a href="#">${element[6]['value'].name}</a>   </td>
        <td class="text-center">
      <a href="#" title="Delete" class="gray-s" onclick="deleteLecture(${index})"><i class="uil uil-trash-alt"></i></a>
        </td>
        </tr>`
    });
    $("#tbodylecture").html(tr);

}

function deleteLecture(index) {
    LectureData.splice(index, 1);

    addLectureToHtml()
}

function FinalCourseContent() {

    var title = $("#ContentTitle").val()
    var uri = $("#ContentFormURL").val()

    if (!title) {
        alert("Please enter a title")
        return false;
    }
    const tn = LectureData.length
    if (tn < 1) {

        alert("Please add at least one lecture")
    }
    for (let i = 0; i < LectureData.length; i++) {
        const f = LectureData[i];

        f.forEach(ele => {

            if (ele.name !== 'file_ext') {
                LectureFormData.append(`lectures_${i+1}_${ele.name}`, ele.value)

            }
        });
    }
    LectureFormData.append('title', title);
    LectureFormData.append('lectures_length', LectureData.length);
    LectureFormData.append('courseid', $("#courseid").val());
    $.ajax({
        url: uri,
        data: LectureFormData,
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        success: function (data, textStatus, jqXHR) {

            Snackbar.show({
                text: "Course Content Added. please wait while refresh.",
                pos: 'bottom-center'
            });
            setTimeout(() => {
                location.reload()
            }, 1000);
        }
    });
}

function submitForm(id) {

    $(id).trigger("submit");
}

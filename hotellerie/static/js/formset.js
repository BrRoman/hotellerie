$(function () {
    $('.formset_row_mail').formset({
        addText: 'Ajouter un mail',
        deleteText: 'Supprimer',
        prefix: 'mail_personne',
    });

    $('.formset_row_tel').formset({
        addText: 'Ajouter un téléphone',
        deleteText: 'Supprimer',
        prefix: 'tel_personne',
    });
});
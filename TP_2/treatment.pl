/* Axiomas (invariantes del dominio) */

check(phosgene_inhalation) :-
    inhalation_dose(unknown),
    writeln('Analizar dosis inhalada.'), !.

check(signs_symptoms) :-
    check(phosgene_inhalation);
    symptoms(unknown),
    writeln('Verificar presencia de señales o síntomas.').

check(chest_xray) :-
    check(phosgene_inhalation);
    (symptoms(true);
    (inhalation_dose(D), D < 150, D >= 50)),
    xray_ans(unknown), 
    writeln('8 hour observation and chest X-ray.');
    check(signs_symptoms).

treatment(symptomatic) :- 
    (irritation(eyes); irritation(upper_airways)), writeln('Symptomatic treatment.'); 
    check(phosgene_inhalation).

treatment(none) :-
    (symptoms(false), inhalation_dose(D), D < 50 ; 
    xray_ans(clear_false)),
    writeln('Discharge with patient discharge instructions');
    check(signs_symptoms); check(chest_xray).

treatment(observation24) :-
    xray_ans(clear_true),
    writeln('Observe/Monitor 24 hours.');
    check(chest_xray).

treatment(early) :-
    inhalation_dose(D), D > 150, writeln('Early treatment');
    check(phosgene_inhalation).

treatment(immediate) :- 
    pulmonary_edema(true),
    writeln('Immediate treatment');
    check(phosgene_inhalation).

/* Ground Facts de instancia variables (podrian resolverse mediante sensado o agregando la informacion interactivamente a la base de conocimientos) */

:- dynamic irritation/1.
:- dynamic inhalation_dose/1.
:- dynamic symptoms/1.
:- dynamic xray_ans/1.
:- dynamic pulmonary_edema/1.

inhalation_dose(unknown).
irritation(unknown).
pulmonary_edema(unknown).
symptoms(unknown).
xray_ans(unknown). 
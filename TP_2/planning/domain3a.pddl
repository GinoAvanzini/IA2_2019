(define (domain air-transport)
    (:predicates (LOAD ?x) (PLANE ?x) (AIRPORT ?x)
        (in ?x ?y) (at ?x ?y))
    
    (:action fly :parameters (?p ?from ?to)
        :precondition (and (PLANE ?p) (AIRPORT ?from) (AIRPORT ?to)
        (at ?p ?from))
        :effect (and (not (at ?p ?from)) (at ?p ?to)))
    
    (:action load :parameters (?c ?p ?a)
        :precondition (and (LOAD ?c) (PLANE ?p) (AIRPORT ?a)
        (at ?c ?a) (at ?p ?a))
        :effect (and (not (at ?c ?a)) (in ?c ?p)))

    (:action unload :parameters (?c ?p ?a)
        :precondition (and (PLANE ?p) (LOAD ?c) (AIRPORT ?a)
        (in ?c ?p) (at ?p ?a))
        :effect (and (at ?c ?a) (not (in ?c ?p)))))
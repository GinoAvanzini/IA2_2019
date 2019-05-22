(define (problem air-transport-task)
    
    (:domain air-transport)
    
    (:objects c1 c2 p1 p2 jfk sf0)
    
    (:init (LOAD c1) (LOAD c2)
        (PLANE p1) (PLANE p2)
        (AIRPORT jfk) (AIRPORT sf0)
        (LOAD c1) (LOAD c2)
        (at c2 jfk) (at p1 sf0) (at p2 jfk))
    
    (:goal (and (at c1 jfk)
        (at c2 sf0))))
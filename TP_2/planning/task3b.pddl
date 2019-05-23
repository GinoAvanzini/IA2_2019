(define (problem capp) 

    (:domain capp)

    (:objects p b1 b2 b3 f1 f2 f3
        h1 h2 h3 r1 r2 r3 a m)

    (:init (CUERPO p) 
        (HERRAMIENTA b1) (HERRAMIENTA b2) (HERRAMIENTA b3)
        (HERRAMIENTA f1) (HERRAMIENTA f2) (HERRAMIENTA f3)
        (ARMARIO a) (HUSILLO m)
        (AGUJERO h1) (AGUJERO h2) (AGUJERO h3)
        (RANURA r1) (RANURA r2) (RANURA r3)
        (en f1 m) (en b1 a) (en b2 a) (en b3 a) (en f2 a) (en f3 a)
        (vinculo b1 h1) (vinculo b2 h2) (vinculo b3 h3)
        (vinculo f1 r1) (vinculo f2 r2) (vinculo f3 r3)
        (not (en p h1)) (not (en p h2)) (not (en p h3))
        (not (en p r1)) (not (en p r2)) (not (en p r3))
    )

    (:goal (and
        (en p h1) (en p h2) (en p h3)
        (en p r1) (en p r2) (en p r3)
        )
    )
)
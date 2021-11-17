;; À copier/coller sur https://compsys-tools.ens-lyon.fr/z3/ ou
;;                                                        en ligne de commande
;;
;; Problème des n dames avec n = 2

(declare-const x00 Bool)
(declare-const x01 Bool)
(declare-const x10 Bool)
(declare-const x11 Bool)

(assert (or x00 x01))
(assert (or x10 x11))

(assert (or (not x00) (not x01)))
(assert (or (not x10) (not x11)))

(assert (or (not x00) (not x10)))
(assert (or (not x01) (not x11)))

(assert (or (not x01) (not x10)))
(assert (or (not x00) (not x11)))

(check-sat)


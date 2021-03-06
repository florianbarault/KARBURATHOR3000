CREATE  DATABASE IF NOT EXISTS IENAC20_KARBURATHOR3000;CREATE  DATABASE IF NOT EXISTS IENAC20_KARBURATHOR3000;





CREATE TABLE `aerodrome` (
  `OACI` varchar(5) NOT NULL,
  `nom_ad` varchar(100) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



INSERT INTO `aerodrome` (`OACI`, `nom_ad`, `latitude`, `longitude`) VALUES
('LFAB', 'DEP LFAB', 49.8787, 1.09516),
('LFAT', 'LFAT DEP/ARR LE TOUQUET', 50.5301, 1.586),
('LFAV', 'DEP LFQI/LFAV', 50.2511, 3.14644),
('LFAY', 'DEP ARR AMIENS', 49.8673, 2.37506),
('LFBA', 'DEP AGEN', 44.1623, 0.598357),
('LFBC', 'LFBC DEP. CAZAUX', 44.5351, -1.12234),
('LFBD', 'LFBD DEP. BORDEAUX', 44.8349, -0.711216),
('LFBE', 'DEP BERGERAC', 44.8172, 0.527554),
('LFBG', 'COGNAC ARR.DEP.', 45.6815, -0.309158),
('LFBH', 'LFBH DEP. LA ROCHELLE', 46.1884, -1.17586),
('LFBI', 'DEP LFBI', 46.5851, 0.324649),
('LFBK', 'DEP LFBK', 46.2344, 2.35925),
('LFBL', 'LFBL DEP. LIMOGES', 45.8689, 1.18785),
('LFBM', 'DEP LFBM', 43.915, -0.48798),
('LFBN', 'DEP LFBN', 46.3181, -0.392314),
('LFBO', 'LFBO DEP. TOULOUSE', 43.6327, 1.36875),
('LFBP', 'LFBP DEP. PAU', 43.3781, -0.400189),
('LFBR', 'DEP LFBR/LFBF', 43.4432, 1.27331),
('LFBS', 'DEP BISCAROSSE', 44.3642, -1.12441),
('LFBT', 'LFBT DEP. TARBES', 43.1806, -0.0104279),
('LFBU', 'DEP LFBU', 45.738, 0.227512),
('LFBX', 'DEP PERIGUEUX', 45.1992, 0.820287),
('LFBZ', 'LFBZ DEP. BIARRITZ', 43.4613, -1.5143),
('LFCC', 'DEP ARR CAHORS/LALBENQUE', 44.3525, 1.49427),
('LFCF', 'ARR DEP FIGEAC', 44.6689, 1.7918),
('LFCI', 'DEPART ALBI', 43.8973, 2.12214),
('LFCK', 'DEP CASTRES', 43.4933, 2.33333),
('LFCL', 'LASBORDES', 43.5799, 1.50554),
('LFCM', 'MILLAU', 43.8944, 3.15324),
('LFCR', 'DEP RODEZ', 44.4005, 2.47121),
('LFCY', 'DEP ROYAN MEDIS', 45.6375, -0.948092),
('LFDB', 'ARR DEP MONTAUBAN', 44.0281, 1.38698),
('LFDN', 'ARR DEP ROCHEFORTSTAGNANT', 45.8976, -0.976668),
('LFDV', 'UL65', 46.2679, 0.19385),
('LFEA', 'ARR/DEP BELLE ILE', 47.3409, -3.18655),
('LFEB', 'DINAN', 48.4514, -2.08872),
('LFEC', 'OUESSANT', 48.4702, -5.04401),
('LFED', 'ARR/DEP PONTIVY', 48.0569, -2.90076),
('LFEI', 'ARR DEP BRIARE', 47.6184, 2.77227),
('LFEQ', 'ARR DEP QUIBERON', 47.49, -3.08277),
('LFER', 'ARR/DEP REDON', 47.7066, -2.0249),
('LFES', 'ARR/DEP GUISCRIFF SCAER', 48.0559, -3.65308),
('LFFI', 'ARR DEP ANCENIS', 47.4034, -1.16438),
('LFFW', 'ARR DEP MONTAIGU', 46.9401, -1.30446),
('LFGA', 'ARR/DEP COLMAR/HOUSSEN', 48.1036, 7.33019),
('LFGB', 'ARR/DEP MULHOUSE/HABSHEIM', 47.7402, 7.40181),
('LFGC', 'ARR/DEP STRASBOURG NEUHOF', 48.5525, 7.75432),
('LFGG', 'ARR/DEP BE LFORT/CHAUX', 47.7025, 6.79791),
('LFGQ', 'ARRIVEE SEMUR', 47.8043, 4.56277),
('LFHP', 'LFHP ARR/DEP LE PUY', 45.0199, 3.80348),
('LFHS', 'BOURG CEYREZIAT', 46.2048, 5.27349),
('LFJB', 'ARR DEP MAULEON', 46.9044, -0.684974),
('LFJR', 'ANGERS MARCE', 47.5705, -0.311436),
('LFKB', 'LFKB DEP BASTIA', 42.5487, 9.46365),
('LFKC', 'LFKC DEP CALVI', 42.5109, 8.77847),
('LFKF', 'DEPART FIGARI', 41.4943, 9.08784),
('LFKJ', 'LFKJ DEP AJACCIO', 41.9083, 8.78562),
('LFKS', 'LFKS DEP SOLENZARA', 41.9258, 9.36515),
('LFLA', 'DEPART AUXERRE', 47.8562, 3.49587),
('LFLB', 'LFLB DEP CHAMBERY', 45.6387, 5.87129),
('LFLC', 'DEP LFLC CLERMONT FD.', 45.7818, 3.15573),
('LFLJ', 'COURCHEVEL', 45.3963, 6.62182),
('LFLL', 'DEP LYON SATOLAS', 45.7153, 5.06733),
('LFLM', 'DEP./ARR. MACON', 46.3059, 4.81176),
('LFLN', 'ST-YAN DEPART', 46.4197, 4.0107),
('LFLO', 'LFLO DEPART ROANNE', 46.051, 4.01218),
('LFLP', 'ARR ANNECY', 45.9376, 6.08418),
('LFLS', 'LFLS DEP GRENOBLE STGEOIR', 45.3491, 5.31696),
('LFLU', 'DEPART VALENCE', 44.9178, 4.95215),
('LFLV', 'LFLV DEP VICHY', 46.1664, 3.39453),
('LFLW', 'DEP LFLW', 44.9039, 2.40921),
('LFLX', 'DEP LFLX', 46.8713, 1.73014),
('LFLY', 'LFLY DEP LYON/BRON', 45.7367, 4.92712),
('LFMC', 'DEP LE LUC LE CANNET', 43.3833, 6.34828),
('LFMD', 'DEPART CANNES', 43.5829, 6.98046),
('LFMH', 'DEP/ARR ST ETIENNE', 45.5339, 4.29058),
('LFMI', 'LFMI DEP ISTRES', 43.5169, 4.90059),
('LFMK', 'DEP CARCASSONNE', 43.161, 2.3088),
('LFML', 'LFML DEP MARSEILLE', 43.4282, 5.21714),
('LFMN', 'LFMN DEP NICE', 43.6633, 7.19751),
('LFMO', 'ORANGE', 44.147, 4.85411),
('LFMP', 'LFMP DEP PERPIGNAN', 42.7288, 2.85689),
('LFMQ', 'LE CASTELLET DEP/ARR', 43.2503, 5.77364),
('LFMT', 'DESSERTE SLCT MONTPELLIER', 43.5802, 3.93954),
('LFMU', 'DEP BEZIERS', 43.3269, 3.34203),
('LFMV', 'DEPART AVIGNON', 43.8951, 4.86785),
('LFMW', 'ARR/DEP CASTELNAUDARY', 43.3129, 1.9275),
('LFMX', 'SAINT AUBAN', 44.0616, 5.97213),
('LFMY', 'SALON DE PROVENCE', 43.6111, 5.09027),
('LFNB', 'DEPART MEN', 44.502, 3.52622),
('LFOA', 'LFOA DEP AVORD', 47.0524, 2.62281),
('LFOC', 'DEP LFOC', 48.056, 1.38091),
('LFOG', 'ARR DEP FLERS/SAINT-PAUL', 48.7512, -0.590866),
('LFOH', 'LE HAVRE ARR DEP SURV', 49.5959, 0.189254),
('LFOM', 'ARR/DEP LESSAY', 49.1931, -1.48167),
('LFOO', 'ARR/DEP SABLES D OLONNE', 46.4855, -1.7034),
('LFOU', 'DEP CHOLET', 47.0883, -0.866763),
('LFOV', 'DEP LAVAL', 48.0366, -0.737855),
('LFOZ', 'ARR/DEP ST DENIS HOTEL', 47.889, 2.15951),
('LFQA', 'REIMS', 49.3151, 4.05258),
('LFQI', 'DEP ARR CAMBRAI', 50.1514, 3.25669),
('LFQP', 'BALISE ARR/DEP', 48.7674, 7.1781),
('LFRB', 'DEP BREST', 48.4564, -4.39134),
('LFRC', 'DEP CHERBOURG', 49.6441, -1.4474),
('LFRD', 'DEP DINARD', 48.5701, -2.04484),
('LFRE', 'ARR/DEP LA BAULE', 47.2892, -2.33408),
('LFRF', 'DEP GRANVILLE', 48.8758, -1.553),
('LFRG', 'ARR-DEP DEAUVILLE', 49.3617, 0.171867),
('LFRH', 'DEP LORIENT-LANN-BIHOUE', 47.7706, -3.4195),
('LFRI', 'DEP LA ROCHE SUR YON', 46.7041, -1.36678),
('LFRJ', 'DEP LANDIVISIAU', 48.5345, -4.1303),
('LFRK', 'DEP CAEN', 49.1595, -0.450225),
('LFRL', 'ARR/DEP LANVEOC', 48.2751, -4.40787),
('LFRM', 'DEPART LE MANS', 47.9502, 0.2047),
('LFRN', 'DEP RENNES', 48.0685, -1.73331),
('LFRO', 'DEP LANNION', 48.7504, -3.46313),
('LFRP', 'DEP PLOERMEL', 48.009, -2.3457),
('LFRQ', 'DEP QUIMPER', 47.9744, -4.15353),
('LFRS', 'DEP NANTES', 47.1553, -1.5964),
('LFRT', 'DEP SAINT-BRIEUC', 48.5208, -2.79955),
('LFRU', 'DEP MORLAIX', 48.6067, -3.79984),
('LFRV', 'DEP VANNES', 47.7235, -2.70681),
('LFRZ', 'DEP SAINT-NAZAIRE', 47.3215, -2.20457),
('LFSH', 'ARR/DEP HAGENAU', 48.7759, 7.79204),
('LFSL', 'DEP LFSL', 45.0355, 1.49666),
('LFSM', 'ARR/DEP MONTBELIARD', 47.4877, 6.76619),
('LFSN', 'ARR NANCY', 48.7048, 6.22006),
('LFSN1', 'DEP NANCY', 48.7052, 6.2065),
('LFTH', 'LFTH DEP HYERES', 43.0946, 6.13221),
('LFTZ', 'LA MOLE', 43.199, 6.47065),
('LFXA', 'AMBERIEU', 45.9695, 5.32522);


CREATE TABLE `avion` (
  `rayonAction` float NOT NULL,
  `consoHoraire` float NOT NULL,
  `idAvion` int(11) NOT NULL,
  `reference` varchar(30) NOT NULL,
  `vitesseCroisiere` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `avion` (`rayonAction`, `consoHoraire`, `idAvion`, `reference`, `vitesseCroisiere`) VALUES
(430, 38, 1, 'DR 400', 215),
(390, 14, 2, 'APM 20', 185),
(645, 60, 3, 'TB-20', 279);


CREATE TABLE `etapes` (
  `idEtape` int(11) NOT NULL,
  `idVol` int(11) NOT NULL,
  `OACIdep` varchar(15) NOT NULL,
  `OACIarr` varchar(15) NOT NULL,
  `OACIdeg` varchar(15) NOT NULL,
  `rang` int(11) NOT NULL,
  `distance` float NOT NULL,
  `carburant` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `etapes` (`idEtape`, `idVol`, `OACIdep`, `OACIarr`, `OACIdeg`, `rang`, `distance`, `carburant`) VALUES
(1, 1, 'LFBL', 'LFLX', 'LFOA', 1, 171.648, 36),
(2, 1, 'LFLX', 'LFEI', 'LFLA', 2, 172.464, 36),
(3, 1, 'LFEI', 'LFGQ', 'LFSN1', 3, 282.211, 53),
(4, 2, 'LFCL', 'LFMW', 'LFMK', 1, 79.997, 14),
(5, 2, 'LFMW', 'LFMU', 'LFMT', 2, 165.308, 20),
(6, 2, 'LFMU', 'LFMI', 'LFMY', 3, 144.737, 19),
(7, 3, 'LFBL', 'LFLX', 'LFOC', 1, 243.908, 63),
(8, 3, 'LFLX', 'LFAY', 'LFAT', 2, 407.433, 100),
(9, 3, 'LFAY', 'LFAV', 'LFQI', 3, 70.557, 25),
(10, 4, 'LFES', 'LFED', 'LFRT', 1, 81.701, 27),
(11, 4, 'LFED', 'LFEB', 'LFRD', 2, 85.317, 28);


CREATE TABLE `messages` (
  `idMessage` int(11) NOT NULL,
  `date` date NOT NULL,
  `idUtilisateur` int(11) NOT NULL,
  `contenu` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `messages` (`idMessage`, `date`, `idUtilisateur`, `contenu`) VALUES
(1, '2021-05-07', 3, 'Trop bien ce site !!'),
(2, '2021-05-30', 2, 'Un grand merci ?? Jacques sans qui ce projet n\'aurait pas ??t?? possible'),
(3, '2021-05-30', 3, 'Vous avez essay?? de cliquer sur l\'ic??ne facebook dans le footer ?');


CREATE TABLE `utilisateurs` (
  `idUtilisateur` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mdp` varchar(30) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `prenom` varchar(50) NOT NULL,
  `certification` varchar(30) NOT NULL,
  `statut` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `utilisateurs` (`idUtilisateur`, `email`, `mdp`, `nom`, `prenom`, `certification`, `statut`) VALUES
(1, 'admin@enac.fr', 'admin', '', '', '', 'admin'),
(2, 'clement.d@gmail.com', 'cl3m3nt', 'deheunynck', 'clement', 'PPL', 'user'),
(3, 'bob.d@gmail.com', 'b0b123', 'dupont', 'bob', 'LAPL', 'user');


CREATE TABLE `vol` (
  `idvol` int(11) NOT NULL,
  `idAvion` int(11) NOT NULL,
  `date` date NOT NULL,
  `idUtilisateur` int(11) NOT NULL,
  `vitesseVent` float NOT NULL,
  `directionVent` float NOT NULL,
  `typeVol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO `vol` (`idvol`, `idAvion`, `date`, `idUtilisateur`, `vitesseVent`, `directionVent`, `typeVol`) VALUES
(1, 1, '2021-05-14', 2, 30, 270, 'vfr_local_vue'),
(2, 2, '2020-07-15', 2, 25, 300, 'nav_vfr'),
(3, 3, '2021-05-12', 3, 10, 20, 'vfr_nuit'),
(4, 3, '2021-05-15', 3, 15, 90, 'vfr_local_hors_aero');


ALTER TABLE `aerodrome`
  ADD PRIMARY KEY (`OACI`);

ALTER TABLE `avion`
  ADD PRIMARY KEY (`idAvion`);

ALTER TABLE `etapes`
  ADD PRIMARY KEY (`idEtape`),
  ADD KEY `idVol` (`idVol`),
  ADD KEY `OACIarr` (`OACIarr`),
  ADD KEY `OACIdeg` (`OACIdeg`),
  ADD KEY `OACIdep` (`OACIdep`);

ALTER TABLE `messages`
  ADD PRIMARY KEY (`idMessage`),
  ADD KEY `idUtilisateur` (`idUtilisateur`);

ALTER TABLE `utilisateurs`
  ADD PRIMARY KEY (`idUtilisateur`);

ALTER TABLE `vol`
  ADD PRIMARY KEY (`idvol`),
  ADD KEY `idAvion` (`idAvion`),
  ADD KEY `idUtilisateur` (`idUtilisateur`);

ALTER TABLE `avion`
  MODIFY `idAvion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `etapes`
  MODIFY `idEtape` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

ALTER TABLE `messages`
  MODIFY `idMessage` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `utilisateurs`
  MODIFY `idUtilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `vol`
  MODIFY `idvol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `etapes`
  ADD CONSTRAINT `etapes_ibfk_1` FOREIGN KEY (`idVol`) REFERENCES `vol` (`idvol`),
  ADD CONSTRAINT `etapes_ibfk_2` FOREIGN KEY (`OACIarr`) REFERENCES `aerodrome` (`OACI`),
  ADD CONSTRAINT `etapes_ibfk_3` FOREIGN KEY (`OACIdeg`) REFERENCES `aerodrome` (`OACI`),
  ADD CONSTRAINT `etapes_ibfk_4` FOREIGN KEY (`OACIdep`) REFERENCES `aerodrome` (`OACI`);


ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`idUtilisateur`) REFERENCES `utilisateurs` (`idUtilisateur`);

ALTER TABLE `vol`
  ADD CONSTRAINT `vol_ibfk_1` FOREIGN KEY (`idAvion`) REFERENCES `avion` (`idAvion`),
  ADD CONSTRAINT `vol_ibfk_2` FOREIGN KEY (`idUtilisateur`) REFERENCES `utilisateurs` (`idUtilisateur`);

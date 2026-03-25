<?php
 error_reporting(E_ALL);
ini_set('display_errors', 1);
require __DIR__ . '/sources/db/db.php'
?>


<!DOCTYPE html>
<html lang="fr">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Portfolio Artiste</title>

	<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Montserrat:wght@300;400&display=swap" rel="stylesheet">
	<link rel="stylesheet" href="sources/hearder_and_body.css">
	<link rel="stylesheet" href="sources/index.css">

</head>

<body>
	<?php 
		include("header.php")
	?>

	<section id="home" class="hero">
		<div class="title_container">
			<h1>Agnes Couret</h1>
			<p>Entrez et laissez vous raconter....</p>
		</div>
	</section>

	<section class="gallery-container">
		<h2 class="section-title">Galerie</h2>
		<div class="gallery">
			<?php
				$sql = "SELECT * FROM category";
				$produits = $pdo->query($sql)->fetchAll(PDO::FETCH_ASSOC);
			foreach ($produits as $produit): ?>
				<h2>Collection <?= $produit["name"]?></h2>
				<a href="./collection.php?category=<?= $produit['id_category'] ?>">	
					<div class="artwork">
						<img src="sources/imgs/<?= $produit["img_link"] ?>">
						<div class="overlay"><?= $produit['name'] ?></div>
					</div>
				</a>
			<?php endforeach; ?>
		</div>
	</section>

	<section id="about">
		<h2 class="section-title">À propos de l'artiste</h2>

		<div class="about">
			<img src="sources/imgs/agnes.jpg">
			<div>
				<p>
					Agnès Couret développe un univers singulier où la pierre brute rencontre la délicatesse du monde animal, 
					créant des œuvres en mosaïque qui célèbrent la beauté sauvage et la poésie des matières naturelles.<br>
					Son parcours artistique s'inscrit dans une trajectoire peu conventionnelle. 
					Après de longues années dédiées à la musique, où elle a cultivé sa sensibilité artistique , 
					Agnès opère un tournant décisif en se tournant vers la mosaïque. <br>Ce changement de discipline n'est pas 
					une rupture mais plutôt une continuité : elle transpose dans la matière cette même recherche d'équilibre, 
					de composition et d'émotion qu'elle explorait par le son.Autodidacte passionnée, elle construit sa pratique
					pas à pas, animée par une soif d'apprentissage insatiable. <br>
					<br>
					Elle se forme à travers différents stages qui 
					lui permettent de découvrir un éventail de techniques, dont la mosaïque en relief, une approche qui donne 
					vie et volume à ses créations. Cette quête de savoir-faire l'amène à explorer sans cesse de nouvelles voies,
					refusant de se cantonner aux méthodes traditionnelles.C'est la rencontre des matières qui nourrit son 
					inspiration. Attirée par la beauté brute et organique de la pierre naturelle, autant que par la 
					transparence lumineuse et la fragilité du verre, Agnès aime orchestrer ces matériaux contrastés dans des 
					portraits animaliers saisissants. Ses œuvres capturent l'essence de ses sujets : la force tranquille d'un 
					oiseau, l'intensité d'un regard, la grâce d'une posture. Dans chaque mosaïque, elle parvient à insuffler 
					une présence, une âme.Son approche créative se caractérise par une curiosité sans limites et un goût
					prononcé pour l'expérimentation. Loin des sentiers battus, elle cherche activement à découvrir et à
					pratiquer des techniques peu usitées dans le domaine de la mosaïque. 
					<br><br>
					Elle détourne volontiers des 
					matériaux de leur usage premier, transformant l'inattendu en composantes essentielles de son vocabulaire 
					plastique. Cette audace lui permet de repousser les frontières de son art et de créer des pièces 
					résolument originales.À travers son travail, Agnès Couret nous invite à porter un regard renouvelé 
					sur le monde animal et sur la matière elle-même, révélant dans chaque fragment de pierre ou de verre 
					une part de beauté insoupçonnée. 
				</p>

				<p>
				Chaque œuvre est une recherche entre texture, lumière et mouvement.<br>
				</p>
			</div>
		</div>
	</section>

	<section id="exhibitions" class="exhibitions">
		<div class="pair">
			<div class="section">
				<h2 class="section-title">Prix et recompenses</h2>
				
				<div class="exhibition-item">
					<strong>2025</strong> — Galerie Moderne, Paris
				</div>
				
				
			</div>
			<div class="section">
				<h2 class="section-title">Expositions solo</h2>
				<div class="exhibition-item">
					<strong>2025</strong> — Galerie Moderne, Paris
				</div>
				
				<div class="exhibition-item">
					<strong>2024</strong> — Salon des Artistes Contemporains
				</div>
				
				<div class="exhibition-item">
					<strong>2023</strong> — Exposition Collective, Marseille
				</div>
			</div>
		</div>

		<div class="pair">
			<div class="section">
				<h2 class="section-title">Expositions collectives</h2>
				<div class="exhibition-item">
					<strong>2025</strong> — Galerie Moderne, Paris
				</div>
				
				<div class="exhibition-item">
					<strong>2024</strong> — Salon des Artistes Contemporains
				</div>
				
				<div class="exhibition-item">
					<strong>2023</strong> — Exposition Collective, Marseille
				</div>
			</div>
			
			<div class="section">

				<h2 class="section-title">Publications et presse</h2>
				<div class="exhibition-item">
					<strong>2025</strong> — Galerie Moderne, Paris
				</div>
				
				<div class="exhibition-item">
					<strong>2024</strong> — Salon des Artistes Contemporains
				</div>
				
				<div class="exhibition-item">
					<strong>2023</strong> — Exposition Collective, Marseille
				</div>
				<div class="exhibition-item">
					<strong>2025</strong> — Galerie Moderne, Paris
				</div>
				
				<div class="exhibition-item">
					<strong>2024</strong> — Salon des Artistes Contemporains
				</div>
				
				<div class="exhibition-item">
					<strong>2023</strong> — Exposition Collective, Marseille
				</div>
			</div>
		</div>	
	</section>

	<section id="contact" class="contact">

		<h2 class="section-title">Contact</h2>

		<input type="text" placeholder="Nom"><br>
		<input type="email" placeholder="Email"><br>
		<textarea rows="5" placeholder="Message"></textarea><br>

		<button>Envoyer</button>
	</section>

	<footer>
		<div class="tag">
			© 2026 Portfolio Artiste
		</div>
		<div class="social">
			<a href="#" class="facebook">
				<img src="./sources/imgs/facebook.png" alt="">
			</a>
			<a href="#" class="instagram">
				<img src="./sources/imgs/instagram.png" alt="">
			</a>
			<a href="#" class="art_majeur">
				<img src="./sources/imgs/facebook.png" alt="">
			</a>
		</div>

	</footer>

	<div class="lightbox" id="lightbox">
		<img id="lightbox-img">
	</div>

	<script>
		const toggle = document.getElementById("menu-toggle")
		const nav = document.getElementById("nav")

		toggle.addEventListener("click",()=>{
		nav.classList.toggle("active")
		})
	</script>
</body>
</html>
document.addEventListener("DOMContentLoaded", () => {
        const grids = document.querySelectorAll(
          ".services-grid, .pricing-grid",
        );
        const cards = document.querySelectorAll(".service-card, .price-card");

        cards.forEach((card) => {
          // Remover cualquier atributo viejo
          card.removeAttribute("data-glow");

          // Crear el borde luminoso
          const glowEl = document.createElement("div");
          glowEl.className = "glow-border";
          card.appendChild(glowEl);
        });

        grids.forEach((grid) => {
          // Solo rastreamos el mouse cuando está sobre la grilla (mejor rendimiento y sin delay)
          grid.addEventListener("mousemove", (e) => {
            // Buscamos las cards específicas dentro de la grilla sobre la que está el mouse
            const gridCards = grid.querySelectorAll(
              ".service-card, .price-card",
            );

            gridCards.forEach((card) => {
              const rect = card.getBoundingClientRect();

              // Coordenadas locales de la tarjeta
              const x = e.clientX - rect.left;
              const y = e.clientY - rect.top;

              card.style.setProperty("--mouse-x", `${x}px`);
              card.style.setProperty("--mouse-y", `${y}px`);
            });
          });
        });

        /* ================= ANIMACIONES DE ENTRADA SCROLL ================= */
        const observerOptions = {
          root: null,
          rootMargin: "0px",
          threshold: 0.15, // 15% del elemento debe ser visible para activarse
        };

        const observer = new IntersectionObserver((entries, observer) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target); // Solo animar una vez
            }
          });
        }, observerOptions);

        const animatedElements = document.querySelectorAll("[data-animation]");
        animatedElements.forEach((el) => observer.observe(el));
      });

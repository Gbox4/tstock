# Maintainer: Your Name <gabriel.t.banks@gmail.com>
pkgname=tstock
pkgver=1.0
pkgrel=1
pkgdesc="A command-line tool to view stock charts in the terminal."
arch=(x86_64)
url="https://github.com/Gbox4/tstock"
license=('GPL')
depends=(glibc)
makedepends=(git make glibc)
optdepends=()
provides=(tstock)
source=("git+$url")
md5sums=('SKIP')


build() {
	cd "$pkgname"
	make
}

package() {
	install -Dm755 "$srcdir/tstock/tstock" "$pkgdir/usr/bin/tstock"
}

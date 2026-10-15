# Build the headless Virtual Jaguar test runner (see vjrun.cpp).
#
# Requires a Virtual Jaguar source tree (default $(abspath ../../vendor/virtualjaguar)) that has been
# configured and built the same way the Virtual Jaguar GUI builds it:
#
#   make -f jaguarcore.mak SDL_CFLAGS="-I/usr/include/SDL2 -D_REENTRANT" \
#        QT_CFLAGS="-fPIC $(pkg-config --cflags Qt5Widgets)"    \
#        CXXFLAGS="-O2 -w -std=c++11"
#   make -C src/m68000 CROSS= CFLAGS="-O2 -std=gnu89 -w" INCS="-I. -I./obj"
#
VJ ?= $(abspath ../../vendor/virtualjaguar)
CXX ?= g++
CXXFLAGS ?= -O2 -g -fPIC -std=c++11 -D__GCCUNIX__ -I$(VJ)/src -I/usr/include/SDL2 $(shell pkg-config --cflags Qt5Widgets)
LIBS = $(VJ)/obj/settings_harness.o $(VJ)/obj/log_harness.o $(VJ)/obj/libjaguarcore.a $(VJ)/src/m68000/obj/libm68k.a \
       $(shell pkg-config --libs Qt5Widgets) -lSDL2 -lz -lpthread -lm

all: vjrun

$(VJ)/obj/settings_harness.o: $(VJ)/src/settings.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(VJ)/obj/log_harness.o: $(VJ)/src/log.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

vjrun: vjrun.cpp $(VJ)/obj/libjaguarcore.a $(VJ)/src/m68000/obj/libm68k.a $(VJ)/obj/log_harness.o $(VJ)/obj/settings_harness.o
	$(CXX) $(CXXFLAGS) vjrun.cpp -o $@ $(LIBS)

clean:
	rm -f vjrun

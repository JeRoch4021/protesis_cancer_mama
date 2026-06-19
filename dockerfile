# syntax=docker/dockerfile:1

ARG UBUNTU_VERSION=24.04
ARG NVIDIA_CUDA_VERSION=12.9.1

# Compilación (Builder Stage)
FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION} AS builder

ARG CUDA_ARCHITECTURES=all-major
ENV QT_XCB_GL_INTEGRATION=xcb_egl
ARG FETCHCONTENT_FULLY_DISCONNECTED=OFF
ENV CCACHE_DIR=/colmap/build/.ccache
ENV CCACHE_BASEDIR=/colmap

ENV DEBIAN_FRONTEND=noninteractive

# Instalar herramientas de compilación y dependencias de COLMAP
RUN apt-get update && \
    apt-get install -y \
        ccache \
        cmake \
        ninja-build \
        build-essential \
        libboost-program-options-dev \
        libboost-graph-dev \
        libboost-system-dev \
        libeigen3-dev \
        libopenimageio-dev \
        openimageio-tools \
        libmetis-dev \
        libgoogle-glog-dev \
        libgtest-dev \
        libgmock-dev \
        libsqlite3-dev \
        libglew-dev \
        qt6-base-dev \
        libqt6opengl6-dev \
        libqt6openglwidgets6 \
        libqt6svg6-dev \
        libcgal-dev \
        libceres-dev \
        libcurl4-openssl-dev \
        libssl-dev \
        libmkl-full-dev

# Parche para la configuración de CMake de openimageio en Ubuntu
RUN mkdir -p /usr/include/opencv4

# Copiar el código fuente de COLMAP al contenedor
COPY . /colmap

# Compilar e instalar COLMAP en una carpeta temporal
RUN cd /colmap && \
    mkdir -p build/.ccache && \
    cd build && \
    cmake .. \
        -GNinja \
        -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCHITECTURES} \
        -DCMAKE_INSTALL_PREFIX=/colmap-install \
        -DFETCHCONTENT_FULLY_DISCONNECTED=${FETCHCONTENT_FULLY_DISCONNECTED} \
        -DBLA_VENDOR=Intel10_64lp && \
    ninja install

# Etapa intermedia para exportar la caché de compilación en procesos CI (opcional)
FROM scratch AS cache-export
COPY --from=builder /colmap/build/.ccache/ /.ccache/
COPY --from=builder /colmap/build/_deps/ /_deps/

#
# Entorno de Ejecución (Runtime)
#
FROM nvidia/cuda:${NVIDIA_CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION} AS runtime

ENV DEBIAN_FRONTEND=noninteractive

# Instalar únicamente las librerías compartidas mínimas para ejecutar COLMAP
RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        libboost-program-options1.83.0 \
        libc6 \
        libomp5 \
        libopengl0 \
        libmetis5 \
        libceres4t64 \
        libopenimageio2.4t64 \
        libgcc-s1 \
        libgl1 \
        libglew2.2 \
        libgoogle-glog0v6t64 \
        libqt6core6 \
        libqt6gui6 \
        libqt6widgets6 \
        libqt6openglwidgets6 \
        libqt6svg6 \
        libcurl4 \
        libssl3t64 \
        libmkl-locale \
        libmkl-intel-lp64 \
        libmkl-intel-thread \
        libmkl-core && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Trear COLMAP ya compilado de la etapa anterior a la carpeta del sistema local
COPY --from=builder /colmap-install/ /usr/local/

# Mantener el contenedor encendido esperando que el orquestador le mande tareas
CMD ["tail", "-f", "/dev/null"]
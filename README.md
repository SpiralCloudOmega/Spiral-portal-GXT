# Spiral Portal GXT (SPGX)

A modern web portal application built with Google Web Toolkit (GWT) and ExtGXT (GXT).

## Features

- **Rich UI Components**: Built with ExtGXT for professional web application interfaces
- **Responsive Layout**: BorderLayout with collapsible navigation and adaptive design
- **Portal Architecture**: Modular design with navigation, dashboard, and content areas
- **Professional Styling**: Clean, modern interface with branded header and footer
- **Maven Build System**: Standard Maven project structure with GWT compilation

## Quick Start

### Prerequisites

- Java 11 or higher
- Maven 3.6 or higher
- Modern web browser

### Building the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/SpiralCloudOmega/Spiral-portal-GXT.git
   cd Spiral-portal-GXT
   ```

2. **Build the application**
   ```bash
   ./build.sh
   ```
   
   Or manually:
   ```bash
   mvn clean compile gwt:compile package
   ```

3. **Run the development server**
   ```bash
   mvn jetty:run
   ```

4. **Open in browser**
   Navigate to: `http://localhost:8080/spiral-portal`

### Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/spiralcloud/omega/portal/
│   │       ├── client/           # GWT client-side code
│   │       └── server/           # Server-side code (if needed)
│   ├── resources/
│   │   └── com/spiralcloud/omega/portal/
│   │       └── SpiralPortal.gwt.xml    # GWT module configuration
│   └── webapp/
│       ├── index.html            # Main HTML page
│       └── WEB-INF/
│           └── web.xml           # Web application configuration
```

## Development

### GWT Super Dev Mode

For development with hot reload:

```bash
mvn gwt:devmode
```

### Building for Production

```bash
mvn clean package
```

The resulting WAR file will be in the `target/` directory.

## Technology Stack

- **GWT (Google Web Toolkit)**: 2.10.0
- **ExtGXT (GXT)**: 4.0.3
- **Maven**: Build and dependency management
- **Java**: 11+
- **Jetty**: Development server

## License

This project is part of the Spiral Cloud Omega ecosystem.

---

**SPGX** - Spiral Portal GXT - Professional web portal solution
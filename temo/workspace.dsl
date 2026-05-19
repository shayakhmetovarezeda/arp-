workspace "Course Registration System" "Система записи на курсы" {

    !identifiers hierarchical

    model {
        student = person "Студент" "Записывается на курсы"
        teacher = person "Преподаватель" "Создаёт курсы"

        courseSystem = softwareSystem "Course Registration System" "Микросервисная система управления курсами" {
            webApp = container "Web Application" "HTML/JS" "Интерфейс"

            courseService = container "course-service" "Python/FastAPI" "Каталог курсов" {
                container courseDb "Course Database" "MongoDB" "Хранение курсов и материалов"
            }

            scheduleService = container "schedule-service" "Python/FastAPI" "Расписание" {
                container scheduleDb "Schedule Database" "PostgreSQL" "Расписание и бронирование слотов"
            }

            enrollmentService = container "enrollment-service" "Python/FastAPI" "Запись студентов" {
                container enrollmentDb "Enrollment Database" "PostgreSQL" "Записи студентов на курсы"
            }

            // Связи внутри системы
            webApp -> enrollmentService "Отправляет запросы" "HTTP/REST"
            enrollmentService -> courseService "Проверяет курсы" "HTTP/REST"
            enrollmentService -> scheduleService "Проверяет расписание" "HTTP/REST"

            // Связи с базами данных
            courseService -> courseDb "Reads/Writes" "MongoDB Driver"
            scheduleService -> scheduleDb "Reads/Writes" "JDBC"
            enrollmentService -> enrollmentDb "Reads/Writes" "JDBC"
        }

        // Связи снаружи
        student -> courseSystem.webApp "Использует" "HTTPS"
        teacher -> courseSystem.webApp "Управляет" "HTTPS"
    }

    views {
        systemContext courseSystem "SystemContext" {
            include *
            autoLayout lr
        }

        container courseSystem "Containers" {
            include *
            autoLayout lr
        }

        styles {
            element Person { shape Person }
            element SoftwareSystem { shape RoundedBox }
            element Container { shape RoundedBox }
            relationship Relationship { thickness 4 }
        }
    }

    configuration {
        scope softwaresystem
    }
}